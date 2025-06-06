# Hardening Linux
Panduan ini mencakup langkah-langkah penting untuk mengamankan sistem Linux, termasuk pengaturan firewall, manajemen pengguna, pengamanan SSH, autentikasi dua faktor (MFA), serta audit dasar sistem.

---

## 1. Mengamankan Port dengan UFW (Uncomplicated Firewall)
### 1.1 Instalasi dan Konfigurasi Dasar
```bash
apt update
apt install ufw -y

# Atur aturan default
ufw default deny incoming     # Blokir semua koneksi masuk
ufw default allow outgoing    # Izinkan semua koneksi keluar
```

### 1.2 Menambahkan Aturan Firewall
```bash
ufw allow 22/tcp                                  # Izinkan akses SSH
ufw allow from 192.168.1.10 to any port 22 proto tcp  # Hanya izinkan IP tertentu
ufw limit ssh                                     # Lindungi dari brute-force
```

### 1.3 Aktivasi dan Pemeriksaan
```bash
ufw enable
ufw status verbose
ufw delete 1    # Hapus rule berdasarkan nomor
```

---

## 2. Manajemen User dan Kebijakan Password
### 2.1 Kebijakan Password Expiry
```bash
chage -m 7 -M 90 -W 7 root
```

Edit `/etc/login.defs`:
```
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_WARN_AGE   7
```

Verifikasi kebijakan user:
```bash
chage -l root
adduser test
chage -l test
deluser test
```

### 2.2 Kebijakan Kompleksitas Password
```bash
apt install libpam-pwquality -y

nano /etc/pam.d/common-password
```

Pastikan ada baris berikut:
```
password requisite pam_pwquality.so retry=3 minlen=12 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 enforce_for_root
```

> **Penjelasan:**
> * `retry=3`: Maksimal 3 kali percobaan
> * `minlen=12`: Minimal 12 karakter
> * `ucredit=-1`: Minimal 1 huruf besar
> * `lcredit=-1`: Minimal 1 huruf kecil
> * `dcredit=-1`: Minimal 1 angka
> * `ocredit=-1`: Minimal 1 simbol

### 2.3 Manajemen User dan Hak Akses
```bash
adduser admin
usermod -aG sudo admin
```

Edit hak sudo user menggunakan `visudo`:
```
admin ALL=(ALL) NOPASSWD: /usr/bin/apt update, /usr/sbin/reboot
```

### 2.4 Nonaktifkan Akses Login Shell
Untuk akun layanan (service account), nonaktifkan akses shell:
```bash
usermod -s /usr/sbin/nologin service1
usermod -s /bin/false service1
```

---

## 3. Pengamanan SSH
### 3.1 Nonaktifkan Login Root via SSH
Edit file SSH config:
```bash
nano /etc/ssh/sshd_config
```

Tambahkan atau ubah baris berikut:
```
PermitRootLogin no
MaxAuthTries 3
MaxSessions 3
AllowUsers user1 user2  # Hanya izinkan user tertentu
```

Lalu restart layanan:
```bash
systemctl restart ssh
```

### 3.2 Konfigurasi SSH Key Authentication
```bash
ssh-keygen
ssh-copy-id user1@server
```

Edit `/etc/ssh/sshd_config`:
```
PasswordAuthentication no
PubkeyAuthentication yes
```

> **Catatan:** Dengan SSH key, password tidak dibutuhkan saat login, dan jauh lebih aman dari brute-force.

---

## 4. Setup MFA (Multi-Factor Authentication) unhtuk koneksi ssh
### 4.1 Instalasi dan Konfigurasi Google Authenticator
```bash
apt install libpam-google-authenticator -y

su user1
google-authenticator
```

Ikuti langkah-langkah di terminal dan simpan kode QR atau OTP key di aplikasi seperti **Google Authenticator** atau **Authy**.

### 4.2 Integrasi MFA ke SSH
Edit PAM SSH:
```bash
sudo nano /etc/pam.d/sshd
```

Tambahkan:
```
auth required pam_google_authenticator.so
```

Lalu edit konfigurasi SSH:
```bash
sudo nano /etc/ssh/sshd_config
```

Pastikan opsi berikut aktif:
```
ChallengeResponseAuthentication yes
UsePAM yes
```

Restart SSH:
```bash
systemctl restart ssh
```

![alt text](images/README/image.png)

### 4.3 Membatasi MFA Hanya untuk User Tertentu
Agar hanya user tertentu yang menggunakan MFA (misalnya semua user kecuali `ctf`, `admin`, dan `aria`), tambahkan di `/etc/pam.d/sshd`:

```
auth [success=1 default=ignore] pam_succeed_if.so user notin ctf,admin,aria
auth required pam_google_authenticator.so
```

> **Catatan:** MFA menambah lapisan keamanan penting, terutama jika password atau SSH key bocor.