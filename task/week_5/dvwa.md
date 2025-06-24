# 🛡️ Laporan Praktikum – DVWA (Damn Vulnerable Web Application)

## 1. Informasi Umum

* **Nama Peserta**        : Aria Fatah
* **Tanggal Praktikum**   : 24 Juni 2025
* **Nama Praktikum**      : Web Application Penetration Testing
* **Target Sistem**       : DVWA (Damn Vulnerable Web Application)
* **IP/URL Target**       : [http://localhost:8080](http://localhost:8080)

---

## 2. Tujuan Praktikum

Tujuan dari praktikum ini adalah **mengidentifikasi dan mengeksploitasi kerentanan umum pada aplikasi web**, seperti **XSS, SQL Injection, Command Injection**, dan **CSRF**, menggunakan target vulnerable DVWA.

---

## 3. Tools dan Bahan

- **Tools Utama**:
  - Burp Suite
  - OWASP ZAP
  - Nmap
  - Firefox/Chrome DevTools

- **VM/Lab Environment**:

  - DVWA (Docker container)
  - Kali Linux (attacker machine)

---

## 4. Metodologi Pengujian

Metode pengujian mengacu pada standar **NIST SP 800-115**:

### 1. **Planning**
- Menentukan target DVWA yang berjalan di `localhost:8080`
- Mengatur tools (Burp, Nmap) dan Docker container

### 2. **Discovery**
- Melakukan scanning port menggunakan Nmap
- Mengamati halaman dan form yang tersedia di aplikasi

### 3. **Attack**
- Melakukan serangan injeksi (SQLi, XSS)
- Mengeksploitasi endpoint rentan menggunakan payload

### 4. **Reporting**
- Mendokumentasikan temuan dan rekomendasi mitigasi

---

## 5. Langkah-Langkah Praktikum
1. Menjalankan DVWA menggunakan Docker: 
   ```bash
   docker run -d -p 8080:80 vulnerables/web-dvwa
   ```
2. Mengakses aplikasi di browser `http://localhost:8080`
3. Login dengan akun `admin:password`
4. Klik "Create / Reset Database" untuk memulai
5. Menjalankan scanning port dengan Nmap:
   ```bash
   nmap -sV -p- localhost
   ```
6. Mengintersep form submission dengan Burp Suite
7. Melakukan SQL Injection pada parameter `id`
8. Melakukan XSS pada input komentar
9. Melakukan Command Injection di fitur ping
10. Melakukan simulasi CSRF pada form penggantian password

---

## 6. Temuan dan Analisis

| No | Jenis Kerentanan  | Deskripsi Temuan                  | Dampak                         | Bukti                    |
| -- | ----------------- | --------------------------------- | ------------------------------ | ------------------------ |
| 1  | SQL Injection     | Parameter `id` tidak divalidasi   | Akses database tanpa otorisasi | ![sql\_injection.png](#) |
| 2  | XSS (Stored)      | Input komentar tidak disanitasi   | Eksekusi script di browser     | ![xss\_stored.png](#)    |
| 3  | Command Injection | Input ping menerima shell command | Eksekusi perintah sistem OS    | ![cmd\_injection.png](#) |
| 4  | CSRF              | Tidak ada token validasi form     | Akses tidak sah atas form      | ![csrf.png](#)           |

---

## 7. Rekomendasi Perbaikan

- Gunakan **prepared statement** untuk semua query SQL
- Terapkan **validasi dan sanitasi input** pada form user
- Gunakan **escaping HTML output** untuk mencegah XSS
- Tambahkan **token CSRF** pada setiap form penting
- Gunakan **WAF (Web Application Firewall)** sebagai lapisan tambahan

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
- XSS pop-up
- Command Injection output
- CSRF exploit HTML
- Hasil scan Nmap (log atau screenshot)