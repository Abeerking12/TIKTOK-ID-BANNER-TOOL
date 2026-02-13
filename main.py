import os
import requests
import random
import re
import phonenumbers
import sys
from time import sleep
from threading import Thread, active_count, Lock
from bs4 import BeautifulSoup
from phonenumbers import PhoneNumberFormat
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from emailtools import generate

# --- Rich UI Libraries ---
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.layout import Layout

console = Console()
stats_lock = Lock()

# --- Config & Assets ---
SOFTWARE_NAMES = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
OPERATING_SYSTEMS = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
UA_ROTATOR = UserAgent(software_names=SOFTWARE_NAMES, operating_systems=OPERATING_SYSTEMS, limit=1200)

class TelegramReporter:
    def __init__(self, target):
        self.target = target
        self.success = 0
        self.failed = 0
        self.errors = open('errors.txt', 'a+', encoding='utf-8')
        self.proxy_types = ('http', 'socks4', 'socks5')
        self.timeout = 15

    def get_banner(self):
        banner_text = f"[bold cyan]TELEGRAM MASS REPORTER PRO[/bold cyan]\n[green]Target:[/green] {self.target}\n[yellow]WhatsApp:[/yellow] https://whatsapp.com/channel/0029Vb75PfXChq6SdkyVaF0A"
        return Panel(banner_text, subtitle="[bold red]Status: System Active[/bold red]", border_style="blue")

    def gen_phone(self):
        """Valid international phone number generator"""
        while True:
            try:
                raw = f"+{random.randint(1, 999)}{random.randint(100000000, 999999999)}"
                parsed = phonenumbers.parse(raw)
                if phonenumbers.is_valid_number(parsed):
                    return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
            except: continue

    def get_random_msg(self):
        """Message file se random line pick karna"""
        try:
            with open('message.txt', 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
                return random.choice(lines).replace('{username}', self.target)
        except FileNotFoundError:
            return f"This user @{self.target} is violating terms. Please investigate."

    def execute_report(self, proxy, p_type):
        url = 'https://telegram.org/support'
        ua = UA_ROTATOR.get_random_user_agent()
        
        proxies = {'http': f'{p_type}://{proxy}', 'https': f'{p_type}://{proxy}'}
        
        try:
            session = requests.Session()
            # Initial Get to grab cookies and CSRF (if any)
            res = session.get(url, proxies=proxies, timeout=self.timeout, headers={'User-Agent': ua})
            soup = BeautifulSoup(res.text, 'html.parser')
            form = soup.find('form', action="/support")
            
            if not form: return

            # Payload Preparation
            data = {}
            for inp in form.find_all(['input', 'textarea']):
                name = inp.get('name')
                if not name: continue
                
                if name == 'support_problem': data[name] = self.get_random_msg()
                elif name == 'support_email': data[name] = generate('gmail')
                elif name == 'support_phone': data[name] = self.gen_phone()
                else: data[name] = inp.get('value', '')

            # POST Request
            post_res = session.post(url, data=data, proxies=proxies, timeout=self.timeout, headers={'User-Agent': ua})
            
            with stats_lock:
                if post_res.status_code == 200:
                    self.success += 1
                else:
                    self.failed += 1
        except Exception as e:
            with stats_lock:
                self.failed += 1
                self.errors.write(f"Proxy: {proxy} | Error: {str(e)}\n")

    def proxy_worker(self, p_type, proxy_list):
        for proxy in proxy_list:
            self.execute_report(proxy.strip(), p_type)

    def stats_display(self):
        """Stylish dashboard for real-time stats"""
        with Live(console=console, refresh_per_second=2) as live:
            while True:
                table = Table(title="Live Reporting Dashboard", show_header=True, header_style="bold magenta")
                table.add_column("Metric", style="dim")
                table.add_column("Value", justify="right")
                
                table.add_row("Target Account", f"[bold cyan]{self.target}[/bold cyan]")
                table.add_row("Success Reports", f"[bold green]{self.success}[/bold green]")
                table.add_row("Failed/Blocked", f"[bold red]{self.failed}[/bold red]")
                table.add_row("Active Threads", f"[bold yellow]{active_count()}[/bold yellow]")
                
                live.update(Layout(Panel(table, border_style="green")))
                sleep(2)

    def run(self):
        console.clear()
        console.print(self.get_banner())
        
        # Stats Display Thread
        Thread(target=self.stats_display, daemon=True).start()

        # Multi-Threaded Engine
        while True:
            threads = []
            for pt in self.proxy_types:
                filename = f"{pt}_proxies.txt"
                if os.path.exists(filename):
                    with open(filename, 'r') as f:
                        proxies = f.readlines()
                    
                    # Chunks of 50 proxies per thread for stability
                    for i in range(0, len(proxies), 50):
                        chunk = proxies[i:i+50]
                        t = Thread(target=self.proxy_worker, args=(pt, chunk))
                        t.start()
                        threads.append(t)
            
            for t in threads:
                t.join()
            sleep(5) # Cooldown before next loop

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    target_input = console.input("[bold yellow][?] Enter Target Username/Link: [/bold yellow]")
    
    bot = TelegramReporter(target_input)
    bot.run()
