import requests
from bs4 import BeautifulSoup
import hashlib
import os

# --- CONFIGURATION ---
# 1. Replace with your Telegram Bot Token from @BotFather
TOKEN = "8516558307:AAH9b14JMmizZ0UIuF4Vbir1xfGjtsDEgvk" 
# 2. Replace with your ID from @userinfobot
CHAT_ID = "6274612198" 
# 3. The URL to watch (Beyoncé's official shop/home)
URL = "https://www.beyonce.com"
# 4. A file to remember the last site version
HASH_FILE = "last_hash.txt"

def send_telegram_alert(message):
    """Sends a message to your phone via Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def get_site_hash():
    """Scrapes the site and creates a unique fingerprint of the content."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # We focus on the 'main' section to ignore background code changes
        content = soup.find('main')
        if not content:
            content = soup.body # Fallback if 'main' tag isn't used
            
        return hashlib.md5(str(content).encode('utf-8')).hexdigest()
    except Exception as e:
        print(f"Error fetching site: {e}")
        return None

def main():
    # 1. Get the current fingerprint of the site
    current_hash = get_site_hash()
    if not current_hash:
        return

    # 2. Load the previous fingerprint from our file
    last_hash = ""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            last_hash = f.read().strip()

    # 3. Compare and Notify
    if current_hash != last_hash:
        # If last_hash was empty, it's the first time running
        if last_hash != "":
            msg = f"🚨 BEYONCÉ UPDATE DETECTED!\n\nThe content on {URL} has changed. Act III might be here."
            send_telegram_alert(msg)
            print("Change detected! Alert sent.")
        else:
            print("First run: Fingerprint saved. Watching for changes now...")

        # 4. Save the new fingerprint for next time
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
    else:
        print("No changes detected. Standing by.")

if __name__ == "__main__":
    main()
