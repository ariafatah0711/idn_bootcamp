# 🛡️ Laporan Praktikum – DVWA (Damn Vulnerable Web Application)
## 1. Informasi Umum

- **Nama Peserta**        : Aria Fatah
- **Tanggal Praktikum**   : 24 Juni 2025
- **Nama Praktikum**      : Web Application Penetration Testing
- **Target Sistem**       : DVWA (Damn Vulnerable Web Application)
- **IP/URL Target**       : [http://localhost:8081](http://localhost:8081)
- **DVWA Security Level** : Low

---

## 2. Tujuan Praktikum
Tujuan dari praktikum ini adalah **mengidentifikasi dan mengeksploitasi kerentanan umum pada aplikasi web**, seperti **XSS, SQL Injection, Command Injection**, dan **CSRF**, menggunakan target vulnerable DVWA.

---

## 3. Tools dan Bahan
- **Tools Utama**:
  - Firefox/Chrome DevTools
  - Burp Suite
  - OWASP ZAP
  - Nmap

- **VM/Lab Environment**:
  - DVWA (Docker container)
  - Kali Linux (attacker machine)

---

## 4. Metodologi Pengujian
Metode pengujian mengacu pada standar **NIST SP 800-115**:

1. **Planning**
2. **Discovery**
3. **Attack**
4. **Reporting**

---

## 5. Langkah-Langkah Praktikum
1. Menjalankan DVWA menggunakan Docker: 
   ```bash
   docker run -d --name dvwa -p 8081:80 vulnerables/web-dvwa
   ```
2. Mengakses aplikasi di browser `http://localhost:8081`
3. Login dengan akun `admin:password`
4. Klik "Create / Reset Database" untuk memulai, dan login kembali
5. Menjalankan scanning port dengan Nmap:
   ```bash
   nmap -sCV -T5 localhost -p 8081 -oN nmap
   ```
   ![alt text](images/01_dvwa/image.png)
6. jangan lupa ubah Security Level menjadi Low

#### 1. Brute Force
- jangan lupa setting scope agar lebih enak interceptnya. (bisa coba add scope dulu di target, lalu setting proxy bagian request dan response AND paling bawah enablein)
- Capture request login menggunakan Burp Proxy.
- Kirim ke Intruder.
- Gunakan tipe Cluster Bomb Attack.
- Payload 1: isikan username (admin), Payload 2: list password.
- Gunakan fitur Grep - Match, tambahkan teks yang muncul saat login berhasil (misal: Welcome to the password protected area).
- Jalankan Start Attack (Simple).
![alt text](images/01_dvwa/image-1.png)

#### 2. Command Injection
- saya mencoba melkukan ping ke alamat ip 8.8.8.8
  ![alt text](images/01_dvwa/image-2.png)
- lalu saya coba lakukan command injection
  ```bash
  8.8.8.8> /dev/null 2>&1; ls
  ```
  ![alt text](images/01_dvwa/image-3.png)

#### 3. Cross Site Request Forgery (CSRF)
- Kamu berhasil mengubah password admin lewat serangan CSRF.
- CSRF terjadi saat:
  - Korban masih login
  - Attacker mengirimkan permintaan palsu ke server yang valid karena cookie korban masih aktif
- Pada level Low/Easy, halaman "Change Password" di DVWA:
  - Tidak punya CSRF token
  - Tidak verifikasi bahwa permintaan datang dari form asli
  - Hanya mengecek apakah user login dan data dikirim via POST

### 4. File
- buka webnya dan coba buka page File 1
  ![alt text](images/01_dvwa/image-8.png)
- terdapat paramter page, lalu kita coba lakukan LFI


- dan saya menemukan path yang pas
  ```http://localhost:8081/vulnerabilities/fi/?page=../../../../../../etc/passwd```
  ![alt text](images/01_dvwa/image-9.png)

### 4. SQL Injection
- test parameter 1
  ![alt text](images/01_dvwa/image-4.png)
- test payload sql injection
  ```' OR 1 = 1 #```
  ![alt text](images/01_dvwa/image-5.png)
- kita bisa mendapatkan semua data user
- kita coba mencari passowrdnya dengan payload
  ```' UNION SELECT user, password FROM users #```
  ![alt text](images/01_dvwa/image-6.png)
- lalu decode menggunakan crackstation / cyberchef
  ![alt text](images/01_dvwa/image-7.png)

### 5. 

---

## 6. Temuan dan Analisis

| No | Jenis Kerentanan  | Deskripsi Temuan                  | Dampak                         | Bukti                    |
| -- | ----------------- | --------------------------------- | ------------------------------ | ------------------------ |
| 1  | SQL Injection     | Parameter `id` tidak divalidasi   | Akses database tanpa otorisasi | gambar |

---

## 7. Rekomendasi Perbaikan

- Gunakan **prepared statement** untuk semua query SQL

---

## 8. Evaluasi dan Refleksi
- **Tantangan Utama:**
  Memahami bagaimana payload yang sederhana dapat mengeksploitasi celah keamanan di aplikasi web.
- **Tools yang Tidak Sesuai Ekspektasi:**
  OWASP ZAP tidak berhasil menangkap semua request karena konfigurasi proxy belum disesuaikan dengan benar.
- **Pelajaran Penting:**
  Validasi input adalah pertahanan utama dalam pengembangan aplikasi web yang aman. Selain itu, penggunaan tools seperti Burp Suite sangat membantu dalam identifikasi kerentanan.

---

## 9. Lampiran

> 📎 Sertakan screenshot berikut (dapat ditambahkan sebagai gambar markdown atau file terpisah):

- SQL Injection (screenshot request & response)
  IMG
- XSS pop-up
- Command Injection output
- CSRF exploit HTML
- Hasil scan Nmap (log atau screenshot)