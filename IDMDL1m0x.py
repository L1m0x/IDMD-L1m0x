#!/usr/bin/env python3

# Project: INSTAGRAM DIRECT MESSAGE DELETER v1.2.0
# Author: L1m0x
# License: MIT (See LICENSE file for details)

import os
import sys
import json
import time
import unicodedata
from datetime import datetime
from typing import Any, Dict, List, Optional

if sys.version_info < (3, 6):
    print("ERROR: Python 3.6 or higher required")
    sys.exit(1)

try:
    from instagrapi import Client
    print("✓ instagrapi imported successfully")
except ImportError as e:
    print(f"ERROR: instagrapi not installed: {e}")
    print("Install with: pip install instagrapi")
    sys.exit(1)

SESSION_FILE = "session.json"

def normalize_text(text):
    if not text: return ""
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')
    return text.replace('ς', 'σ')

def get_password():
    """Get password input"""
    try:
        import getpass
        return getpass.getpass("Instagram password (hidden): ")
    except Exception:
        print("Note: Password will be visible")
        return input("Instagram password: ")

def load_session(client: Client, session_file: str) -> bool:
    """Load session"""
    if not os.path.exists(session_file):
        return False
    try:
        client.load_settings(session_file)
        client.account_info()
        return True
    except:
        try:
            os.remove(session_file)
        except:
            pass
        return False

def save_session(client: Client, session_file: str) -> bool:
    """Save session"""
    try:
        client.dump_settings(session_file)
        return True
    except:
        return False

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class IGDMTool:
    def __init__(self):
        self.client = Client()
        self.logged_in = False
        os.system('')
        self.selected_thread_id = None
        self.my_username = None
        self.my_user_id = None
        self.selected_username = "None"
        self.last_matches = []
        print("✓ IGDMTool initialized")
    
    def login(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.PURPLE}{'='*50}{Color.END}")
        print(f"{Color.BOLD}{Color.CYAN}          🔐 INSTAGRAM SECURE LOGIN{Color.END}")
        print(f"{Color.PURPLE}{'='*50}{Color.END}\n")

        if os.path.exists(SESSION_FILE):
            print(f"{Color.YELLOW}⏳ An existing session was detected. Login...{Color.END}")
            try:
                self.client.load_settings(SESSION_FILE)
                info = self.client.account_info()
                self.my_username = info.username
                self.my_user_id = str(info.pk)
                print(f"\n{Color.GREEN}✅ Welcome back, {Color.BOLD}{self.my_username}!{Color.END}")
                self.logged_in = True
                time.sleep(2)
                return True
            except Exception:
                print(f"{Color.RED}✗ Session is closed. Please connect again.{Color.END}\n")

        user = input(f"{Color.BOLD}Username: {Color.END}").strip()
        pwd = input(f"{Color.BOLD}Password: {Color.END}").strip()
        
        print(f"\n{Color.CYAN}📡 Contact Instagram Servers...{Color.END}")
        
        try:
            self.client.login(user, pwd)
            info = self.client.account_info()
            self.my_username = info.username
            self.my_user_id = str(info.pk)
            self.client.dump_settings(SESSION_FILE)
            self.logged_in = True
            print(f"\n{Color.GREEN}✅ LOGIN SUCCESSFUL!{Color.END}")
            print(f"{Color.BLUE}User ID: {self.my_user_id}{Color.END}")
            time.sleep(2)
        except Exception as e:
            print(f"\n{Color.RED}❌ LOGIN FAILED: {e}{Color.END}")
            input(f"\nPress [ENTER] to retry again...")
            
    def list_threads_raw_api(self):
        if not self.logged_in: 
            print(f"{Color.RED}❌ You must first log in (1)!{Color.END}")
            time.sleep(2); return

        os.system('cls' if os.name == 'nt' else 'clear')
        all_threads = []
        cursor = None
        
        while True:
            print(f"{Color.PURPLE}{'='*65}{Color.END}")
            print(f"{Color.BOLD}{Color.CYAN}          📩 FULL DIRECT MESSAGES LIST{Color.END}")
            print(f"{Color.PURPLE}{'='*65}{Color.END}")
            print(f"{Color.BOLD}{'#':<3} | {'USERNAME':<15} | {'THREAD ID':<22}{Color.END}")
            print(f"{Color.PURPLE}{'-'*65}{Color.END}")

            try:
                params = {"persistent_badging": "true"}
                if cursor:
                    params["cursor"] = cursor
                
                response = self.client.private_request("direct_v2/inbox/", params=params)
                inbox = response.get('inbox', {})
                new_threads = inbox.get('threads', [])
                all_threads.extend(new_threads)
                
                for i, t in enumerate(all_threads, 1):
                    t_id = t.get('thread_id')
                    users = t.get('users', [])
                    username = users[0].get('username', 'Unknown') if users else "Group/Saved"
                    
                    row_color = Color.WHITE if i % 2 == 0 else Color.CYAN
                    print(f"{Color.BOLD}{i:<3}{Color.END} | "
                          f"{row_color}{username[:15]:<15}{Color.END} | "
                          f"{Color.YELLOW}{t_id:<22}{Color.END}")

                print(f"{Color.PURPLE}{'='*65}{Color.END}")
                
                cursor = inbox.get('oldest_cursor')
                
                prompt = f"\n{Color.BOLD}Select #, write 'M' for more, or [ENTER] for back: {Color.END}"
                choice = input(prompt).strip().lower()

                if choice == 'm' and cursor:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"{Color.YELLOW}⏳ Loading next list of direct messages...{Color.END}")
                    continue
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(all_threads):
                        self.selected_thread_id = all_threads[idx].get('thread_id')
                        users = all_threads[idx].get('users', [])
                        self.selected_username = users[0].get('username', 'Unknown') if users else "Group"
                        
                        print(f"\n{Color.GREEN}✅ CHOOSEN: {Color.BOLD}{self.selected_username}{Color.END}")
                        time.sleep(1.5)
                        break
                    else:
                        print(f"{Color.RED}✗ Invalid choice.{Color.END}")
                        time.sleep(1)
                else:
                    break

            except Exception as e:
                print(f"\n{Color.RED}❌ ERROR INBOX: {e}{Color.END}")
                input(f"\nPress [ENTER] to go to the previous list...")
                break
                
    def select_thread(self):
        if not self.logged_in: 
            print(f"{Color.RED}❌ You must first log in (Option 1)!{Color.END}")
            time.sleep(2)
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.PURPLE}{'='*50}{Color.END}")
        print(f"{Color.BOLD}{Color.CYAN}          🎯 TARGET SELECTION (THREAD){Color.END}")
        print(f"{Color.PURPLE}{'='*50}{Color.END}\n")

        name = input(f"{Color.BOLD}Enter the recipient's Username: {Color.END}").strip().lower()
        print(f"\n{Color.YELLOW}🔍 Search for a chat for the user: {Color.BOLD}{name}...{Color.END}")

        try:
            user_id = self.client.user_id_from_username(name)
            
            threads = self.client.direct_threads(30)
            found_thread = None
            
            for t in threads:
                if str(user_id) in [str(u.pk) for u in t.users]:
                    found_thread = t
                    break

            if found_thread:
                self.selected_thread_id = found_thread.id
                print(f"\n{Color.GREEN}✅ TARGET FOUND!{Color.END}")
                print(f"{Color.BLUE}Thread ID: {self.selected_thread_id}{Color.END}")
                print(f"{Color.CYAN}Chat with: {name}{Color.END}")
                time.sleep(2)
            else:
                print(f"{Color.YELLOW}⚠️ The conversation was not found in recent. Attempting to recover...{Color.END}")
                thread = self.client.direct_thread_by_participants([user_id])
                self.selected_thread_id = getattr(thread, 'id', None) or thread.get('thread_id')
                print(f"\n{Color.GREEN}✅ TARGET LOCKED: {self.selected_thread_id}{Color.END}")
                time.sleep(2)

        except Exception as e:
            print(f"\n{Color.RED}❌ ERROR TRACKING: {e}{Color.END}")
            input(f"\nPress [ENTER] to go to the menu...")

    def fetch_all_messages_paginated(self, max_messages=5000):
        all_messages = []
        cursor = None
        page = 1
        while len(all_messages) < max_messages:
            params = {"visual_message_return_type": "unseen", "direction": "older", "limit": "75"}
            if cursor: params["cursor"] = cursor
            response = self.client.private_request(f"direct_v2/threads/{self.selected_thread_id}/", params=params)
            thread = response['thread']
            items = thread.get('items', [])
            if not items: break
            all_messages.extend(items)
            cursor = thread.get('oldest_cursor') or thread.get('next_cursor')
            if not cursor: break
            time.sleep(0.8)
            page += 1
        return all_messages

    def view_messages_raw_api(self):
        if not self.selected_thread_id:
            print(f"{Color.RED}❌ You must first choose a conversation (2 or 3)!{Color.END}")
            time.sleep(2); return

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.PURPLE}{'='*60}{Color.END}")
        print(f"{Color.BOLD}{Color.CYAN}          💬 RECENT MESSAGES{Color.END}")
        print(f"{Color.PURPLE}{'='*60}{Color.END}")

        try:
            # Παίρνουμε τα τελευταία 50 μηνύματα
            items = self.fetch_all_messages_paginated(50)
            
            if not items:
                print(f"{Color.YELLOW}No messages were found in this conversation.{Color.END}")
            
            for item in reversed(items):
                user_id = str(item.get('user_id'))
                text = item.get('text', '')
                i_type = item.get('item_type')
                
                prefix = f"{Color.GREEN}[{self.my_username}]{Color.END}" if user_id == self.my_user_id else f"{Color.YELLOW}[{self.selected_username}]{Color.END}"
                
                if i_type == 'text':
                    content = text
                elif i_type == 'clip':
                    content = f"{Color.PURPLE}[REEL]{Color.END}"
                elif i_type == 'voice_media':
                    content = f"{Color.BLUE}[VOICE MESSAGE]{Color.END}"
                elif i_type in ['media', 'visual_media']:
                    content = f"{Color.CYAN}[PHOTO/VIDEO]{Color.END}"
                else:
                    content = f"{Color.WHITE}[{i_type.upper()}]{Color.END}"

                print(f"{prefix}: {content}")

            print(f"{Color.PURPLE}{'='*60}{Color.END}")
            
            input(f"\n{Color.BOLD}Press [ENTER] to go to the main menu...{Color.END}")

        except Exception as e:
            print(f"\n{Color.RED}❌ ERROR: {e}{Color.END}")
            input(f"\nPress [ENTER] to go back...")

    def search_messages_raw_api(self):
        if not self.selected_thread_id:
            print(f"{Color.RED}❌ You must first choose a conversation (2)!{Color.END}")
            time.sleep(2)
            return

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.PURPLE}{'='*60}{Color.END}")
        print(f"{Color.BOLD}{Color.CYAN}          📡 FULL SCAN OF MESSAGES{Color.END}")
        print(f"{Color.PURPLE}{'='*60}{Color.END}")
        print(f"{Color.YELLOW}🔍 Start scan... Please wait.{Color.END}\n")

        items = self.fetch_all_messages_paginated(5000)
        self.last_matches = []
        
        count_text = 0
        count_media = 0
        count_reels = 0
        count_voice = 0

        print(f"{Color.BOLD}DATA ASSSIS:{Color.END}")
        print(f"{Color.PURPLE}{'-'*30}{Color.END}")

        for item in items:
            t = item.get('text', '')
            it = item.get('item_type')
            
            is_text = (it == 'text')
            is_reel = (it == 'clip' or 'clip' in item)
            is_voice = (it == 'voice_media' or 'voice_media' in item)
            is_media = (it in ['media', 'visual_media'] or 'media' in item)

            if any([is_text, is_reel, is_voice, is_media]):
                self.last_matches.append(item)
                
                if is_text: 
                    count_text += 1
                    print(f"{Color.GREEN}✓ [TEXT]{Color.END} {t[:30]}...", end="\r")
                elif is_reel: 
                    count_reels += 1
                    print(f"{Color.PURPLE}✓ [REEL] Found Reel!{Color.END}", end="\r")
                elif is_voice: 
                    count_voice += 1
                    print(f"{Color.BLUE}✓ [VOICE] Found Ηχητικό!{Color.END}", end="\r")
                elif is_media: 
                    count_media += 1
                    print(f"{Color.CYAN}✓ [MEDIA] Found Photo/Video!{Color.END}", end="\r")
                
                time.sleep(0.005)

        print(f"\n\n{Color.PURPLE}{'='*60}{Color.END}")
        print(f"{Color.BOLD}{Color.GREEN}✅ The scan is completed!{Color.END}")
        print(f"{Color.PURPLE}{'-'*60}{Color.END}")
        print(f" 📝 Texts:    {Color.BOLD}{count_text}{Color.END}")
        print(f" 🎬 Reels:      {Color.BOLD}{count_reels}{Color.END}")
        print(f" 🎤 Voice Messages:    {Color.BOLD}{count_voice}{Color.END}")
        print(f" 🖼️ Media:      {Color.BOLD}{count_media}{Color.END}")
        
        own_count = len([m for m in self.last_matches if str(m.get('user_id')) == self.my_user_id])
        others_count = len(self.last_matches) - own_count

        print(f"\n{Color.PURPLE}{'='*60}{Color.END}")
        print(f" 🚀 {Color.BOLD}ABOUTIONS REFERRING:{Color.END}")
        print(f" {Color.GREEN}Yours (will be deleted): {Color.BOLD}{own_count}{Color.END}")
        print(f" {Color.RED}Other (They will remain): {Color.BOLD}{others_count}{Color.END}")
        print(f"{Color.PURPLE}{'='*60}{Color.END}")
        print(f" 🚀 {Color.BOLD}TOTAL FOR DELETION: {own_count}{Color.END}")
        print(f"{Color.PURPLE}{'='*60}{Color.END}")
        
        input(f"\n{Color.YELLOW}Press [ENTER] to return after '6' for Delete all messages that was sent...{Color.END}")
                       
    def delete_messages_raw_api(self):
        """Διαγραφή μηνυμάτων με εμφάνιση κειμένου (Live Feedback)"""
        if not self.last_matches: 
            print(f"{Color.RED}❌ There are no messages! Run the Scan first (5).{Color.END}")
            time.sleep(2); return
        
        own = [m for m in self.last_matches if str(m.get('user_id')) == self.my_user_id]
        
        if not own:
            print(f"{Color.YELLOW}⚠️ No messages were found for deletion.{Color.END}")
            time.sleep(2); return

        print(f"\n{Color.PURPLE}{'='*65}{Color.END}")
        print(f"{Color.YELLOW}WILL BE DELETED {Color.BOLD}{len(own)}{Color.END}{Color.YELLOW} MESSAGES.{Color.END}")
        confirm = input(f"{Color.BOLD}Type 'YES' to confirm: {Color.END}").strip()
        
        if confirm == 'YES':
            print(f"\n{Color.CYAN}🚀 Deletion of messages has been started...{Color.END}\n")
            try:
                for i, m in enumerate(own, 1):
                    mid = m.get('item_id')
                    
                    msg_text = m.get('text', '')
                    if not msg_text:
                        msg_text = f"[{m.get('item_type', 'MEDIA').upper()}]"
                    
                    display_text = (msg_text[:30] + '..') if len(msg_text) > 30 else msg_text
                    self.client.private_request(
                        f"direct_v2/threads/{self.selected_thread_id}/items/{mid}/delete/",
                        data={'_uuid': self.client.uuid, '_uid': self.my_user_id, '_csrftoken': self.client.token}
                    )
                    
                    print(f"{Color.RED}[{i}/{len(own)}]{Color.END} {Color.WHITE}ID: {mid[-6:]}{Color.END} | {Color.CYAN}{display_text}{Color.END}")
                    
                    time.sleep(1.5)
                
                print(f"\n{Color.GREEN}✨ Mission Finished successfully!{Color.END}")
                input("\nPress [ENTER] to go back...")
                
            except KeyboardInterrupt:
                print(f"\n\n{Color.YELLOW}🛑 PROCEDURE CONTROL BY THE USER.{Color.END}")
                time.sleep(2)
            except Exception as e:
                print(f"\n{Color.RED}❌ ERROR: {e}{Color.END}")
                time.sleep(2)
        else:
            print(f"\n{Color.WHITE}The deletion has been canceled.{Color.END}")
            time.sleep(1)
            
        self.last_matches = []
    
    def logout(self):
        """Αποσύνδεση και καθαρισμός Session στην επιλογή 8"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.PURPLE}{'='*50}{Color.END}")
        print(f"{Color.BOLD}{Color.RED}          🚪 Logout / Switch instagram account{Color.END}")
        print(f"{Color.PURPLE}{'='*50}{Color.END}\n")
        
        confirm = input(f"{Color.YELLOW}You want to log out of the account {self.my_username}; (y/n): {Color.END}").lower()
        
        if confirm == 'y':
            # Διαγραφή αρχείου session
            if os.path.exists(SESSION_FILE):
                try:
                    os.remove(SESSION_FILE)
                    print(f"{Color.GREEN}✅ The session has been deleted.{Color.END}")
                except: pass
            
            self.client = Client()
            self.logged_in = False
            self.my_username = "None"
            self.my_user_id = None
            self.selected_thread_id = None
            self.selected_username = "None"
            
            print(f"\n{Color.CYAN}Ready to login with different account (Option 1).{Color.END}")
            time.sleep(2)
            
    def menu_loop(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Color.PURPLE}{'='*50}{Color.END}")
            print(f"{Color.BOLD}{Color.CYAN}       🚀 INSTAGRAM DIRECT MESSAGE DELETER v1.2.0{Color.END}")
            print(f"{Color.PURPLE}{'='*50}{Color.END}")
            print(f"{Color.BOLD}{Color.CYAN}              🚀 Created by L1m0x {Color.END}")
            print(f"{Color.PURPLE}{'='*50}{Color.END}")
            
            status = f"{Color.GREEN}Connected as: {self.my_username}" if self.logged_in else f"{Color.RED}Status: Not Logged In"
            print(f" {status}{Color.END}")
            target_display = f"{Color.YELLOW}{self.selected_username}{Color.END} ({Color.WHITE}{self.selected_thread_id}{Color.END})" if self.selected_thread_id else f"{Color.RED}None{Color.END}"
            print(f" 🎯 TARGET: {target_display}")
            
            print(f"{Color.PURPLE}{'-'*50}{Color.END}")
            print(f" {Color.BOLD}[1]{Color.END} Login Account")
            print(f" {Color.BOLD}[2]{Color.END} Full Direct Messages List")
            print(f" {Color.BOLD}[3]{Color.END} Select Target by Username/ID")
            print(f" {Color.BOLD}[4]{Color.END} View Recent Messages")
            print(f" {Color.BOLD}[5]{Color.END} {Color.CYAN}Start a full scan of all messages{Color.END}")
            print(f" {Color.BOLD}[6]{Color.END} {Color.RED}Delete all messages sent{Color.END}")
            print(f" {Color.BOLD}[7]{Color.END} Logout / Switch instagram account")
            print(f" {Color.BOLD}[8]{Color.END} Exit IDMD-L1m0x")
            print(f"{Color.PURPLE}{'='*50}{Color.END}")
            
            choice = input(f"\n{Color.BOLD}Selection > {Color.END}").strip()
            
            if choice == "1": self.login()
            elif choice == "2": self.list_threads_raw_api()
            elif choice == "3": self.select_thread()
            elif choice == "4": self.view_messages_raw_api()
            elif choice == "5": self.search_messages_raw_api()
            elif choice == "6": self.delete_messages_raw_api()
            elif choice == "7": self.logout()
            elif choice == "8": 
                print(f"{Color.YELLOW}Exiting... Fly safe! 🚀{Color.END}")
                break

if __name__ == "__main__":
    try:
        tool = IGDMTool()
        tool.menu_loop()
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}👋 Bye! The missile landed safely.{Color.END}")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
