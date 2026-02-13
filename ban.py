import requests
import time
import re
import os
import sys
import random
from threading import Thread, active_count, Lock

# --- Rich UI Libraries ---
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

console = Console()
stats_lock = Lock()

class TikTokReporter:
    def __init__(self, target):
        self.target = target
        self.success = 0
        self.failed = 0
        self.timeout = 15

    def fake_animation_logic(self):
        """Ye function background mein fake reports ke numbers badhayega"""
        while True:
            if self.target:
                with stats_lock:
                    # Har thori der baad 5 se 20 ke beech random reports add hongi
                    self.success += random.randint(5, 20)
                time.sleep(random.uniform(0.4, 1.2))

    def stats_display(self):
        """Stylish Dashboard jo live update hoga"""
        with Live(console=console, refresh_per_second=4) as live:
            while True:
                table = Table(title="[bold green]⚡ TIKTOK ID BANNER ACTIVE ⚡[/bold green]", header_style="bold cyan")
                table.add_column("Status", justify="center")
                table.add_column("Metric", style="dim")
                table.add_column("Value", justify="right", style="bold green")

                icon = random.choice(["🔥", "⚡", "🚀", "🛡️", "🎯"])

                table.add_row(icon, "Target Account", f"[cyan]@{self.target}[/cyan]")
                table.add_row("✅", "Success Reports", f"[bold green]{self.success}[/bold green]")
                table.add_row("❌", "Failed/Blocked", f"[bold red]{self.failed}[/bold red]")
                table.add_row("📡", "Active Threads", f"[bold yellow]{active_count()}[/bold yellow]")
                
                live.update(Panel(table, border_style="green", title="[bold white]OX CYBER TEAM[/bold white]"))
                time.sleep(0.5)

    def run(self):
        # Fake animation aur stats display ko background threads mein start karein
        Thread(target=self.fake_animation_logic, daemon=True).start()
        Thread(target=self.stats_display, daemon=True).start()

        # Yahan aapka asli reporting loop (agar hai toh) chalega
        while True:
            time.sleep(10)

def banner():
    os.system('clear')
    console.print(Panel("""[bold cyan]
  █████╗ ██████╗ ███████╗███████╗██████╗ 
 ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
 ███████║██████╔╝█████╗  █████╗  ██████╔╝
 ██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗
 ██║  ██║██████╔╝███████╗███████╗██║  ██║
 ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝[/bold cyan]
 [yellow]-------------------------------------------[/yellow]
 [white]WhatsApp: https://whatsapp.com/channel/0029Vb75PfXChq6SdkyVaF0A[/white]
 [white]Telegram: https://t.me/+9qqWl7O_kVUxMmNk[/white]
 [yellow]-------------------------------------------[/yellow]""", border_style="blue"))

if __name__ == "__main__":
    banner()
    target = console.input("[bold yellow][?] Enter Target Username: [/bold yellow]").replace('@', '')
    
    bot = TikTokReporter(target)
    bot.run()

def main():
    banner()
    print(f"{CYAN}[1]{RESET} Auto All-In-One Report")
    print(f"{CYAN}[2]{RESET} Custom Category Report")
    print(f"{CYAN}[3]{RESET} Join Community (Social Links)")
    print(f"{CYAN}[0]{RESET} Exit\n")

    choice = input(f"{YELLOW}[+] Select Option: {RESET}")

    if choice == '1':
        target = input(f"{YELLOW}[+] Enter Target Username (e.g: khaby.lame): {RESET}").replace('@', '')
        start_report(target, '310') # Default mass report code

    elif choice == '2':
        print(f"\n{GREEN}1- Original Report (310)")
        print(f"2- Hate Speech (306)")
        print(f"3- Suicide/Self-Harm (3051){RESET}")
        r_choice = input(f"{YELLOW}[+] Select Type: {RESET}")
        target = input(f"{YELLOW}[+] Enter Target Username: {RESET}").replace('@', '')
        
        reasons = {'1': '310', '2': '306', '3': '3051'}
        if r_choice in reasons:
            start_report(target, reasons[r_choice])
        else:
            print(f"{RED}[!] Invalid Selection.{RESET}")

    elif choice == '3':
        print(f"{GREEN}[*] Opening Links...{RESET}")
        open_links()
        
    elif choice == '0':
        sys.exit()
    else:
        print(f"{RED}[!] Sahi option chunein.{RESET}")

if __name__ == "__main__":
    main()
