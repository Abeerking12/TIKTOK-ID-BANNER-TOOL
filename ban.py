import requests
import time
import re
import os
import sys

# --- ANSI Color Codes for Professional Look ---
GREEN = '\033[1;92m'
RED = '\033[1;31m'
CYAN = '\033[1;36m'
YELLOW = '\033[1;33m'
RESET = '\033[0m'

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""
{CYAN}████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ 
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ 
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝{RESET}
 {YELLOW}---------------------------------------------{RESET}
 {GREEN}[+] WhatsApp:{RESET} https://whatsapp.com/channel/0029Vb75PfXChq6SdkyVaF0A
 {GREEN}[+] Telegram:{RESET} https://t.me/+9qqWl7O_kVUxMmNk
 {YELLOW}---------------------------------------------{RESET}
    """)

def open_links():
    """Social links ko browser mein open karta hai"""
    links = [
        "https://whatsapp.com/channel/0029Vb75PfXChq6SdkyVaF0A",
        "https://t.me/+9qqWl7O_kVUxMmNk"
    ]
    for link in links:
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system(f"termux-open-url {link} 2>/dev/null || xdg-open {link}")
        else:
            os.system(f"start {link}")

def get_page_id(target_id):
    """TikTok username se unique Page ID nikalne ke liye"""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    url = f'https://www.tiktok.com/@{target_id}'
    try:
        req = requests.get(url, headers=headers, timeout=10)
        # Regex to find pageId or uniqueId
        page_id = re.findall('"pageId":"(.*?)"', req.text)
        if not page_id:
            # Alternate search if first fails
            page_id = re.findall('"authorId":"(.*?)"', req.text)
            
        return page_id[0] if page_id else None
    except Exception as e:
        print(f"{RED}[!] Error fetching ID: {e}{RESET}")
        return None

def start_report(target_id, reason_code):
    page_id = get_page_id(target_id)
    
    if not page_id:
        print(f"{RED}[-] Target ID '{target_id}' nahi mil saki. Username check karein.{RESET}")
        return

    print(f"{GREEN}[+] Target Page ID:{RESET} {page_id}")
    print(f"{YELLOW}[*] Reporting started... Press Ctrl+C to stop.{RESET}\n")

    report_url = 'https://www.tiktok.com/node/report/reasons_put'
    
    # Modern Dynamic Parameters
    params = {
        'aid': '1988',
        'app_name': 'tiktok_web',
        'device_platform': 'web',
        'region': 'SA',
        'priority_region': '',
        'os': 'windows'
    }

    # Custom Header to bypass basic detection
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': f'https://www.tiktok.com/@{target_id}',
        'Origin': 'https://www.tiktok.com'
    }

    payload = {
        'object_id': page_id,
        'owner_id': page_id,
        'reason': reason_code,
        'report_type': "user"
    }

    count = 0
    try:
        while True:
            response = requests.post(report_url, params=params, json=payload, headers=headers)
            if response.status_code == 200:
                count += 1
                print(f"{GREEN}[{count}] REPORT SUCCESSFUL (Reason: {reason_code}) 👅{RESET}")
            else:
                print(f"{RED}[!] Failed. Proxy ya Cookie ki zaroorat ho sakti hai.{RESET}")
            
            time.sleep(2) # Speed control
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Reporting stopped by user.{RESET}")

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
