#!/bin/bash

# Colors for styling
CYAN='\033[0;36m'
GREEN='\033[0;92m'
YELLOW='\033[1;33m'
RESET='\033[0m'

clear
echo -e "${CYAN}==========================================${RESET}"
echo -e "${GREEN}   TIKTOK ID BANNER TOOL - AUTO SETUP     ${RESET}"
echo -e "${CYAN}==========================================${RESET}"
echo -e "${YELLOW}[*] Installing requirements...${RESET}"

# Update and Install Python/Pip
pkg install python -y
pip install --upgrade pip

# Install Python Libraries
pip install requests beautifulsoup4 rich phonenumbers random-user-agent emailtools

# Create necessary files if they don't exist
if [ ! -f message.txt ]; then
    echo "This account is spreading hate speech and violating community guidelines." > message.txt
    echo -e "${GREEN}[+] Created default message.txt${RESET}"
fi

touch http_proxies.txt socks4_proxies.txt socks5_proxies.txt
echo -e "${GREEN}[+] Proxy files initialized.${RESET}"

echo -e "${CYAN}------------------------------------------${RESET}"
echo -e "${GREEN}[SUCCESS] Setup Complete! Starting Tool...${RESET}"
echo -e "${CYAN}------------------------------------------${RESET}"
sleep 2

# Final Run
python Run.py
