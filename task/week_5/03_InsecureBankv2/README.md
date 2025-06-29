# InsecureBankv2
## 1. Informasi Umum

- **Nama Peserta**        : Aria Fatah
- **Tanggal Praktikum**   : 29 Juni 2025
- **Nama Praktikum**      : Lab Mobile Application Pentest
- **Target Sistem**       : InsecureBankv2
- **IP/URL Target**       : []()

---

## 2. Tujuan Praktikum
Tujuan dari praktikum ini adalah untuk **mengidentifikasi dan mengeksploitasi berbagai kerentanan umum pada aplikasi mobile**, khususnya pada platform Android. Target dari pengujian ini adalah **InsecureBankv2**, sebuah aplikasi Android yang secara sengaja dibuat dengan kelemahan keamanan untuk kebutuhan pembelajaran dan latihan penetration testing.

Fokus pengujian dalam praktikum ini meliputi:

* **Analisis komunikasi client-server** menggunakan intercepting proxy seperti Burp Suite
* **Bypass login** dan otentikasi yang tidak aman
* **Penyimpanan data sensitif secara lokal** di perangkat
* **Penerapan SSL/TLS yang tidak benar**, termasuk potensi untuk bypass SSL pinning
* **Kerentanan pada endpoint API** seperti kebocoran data atau otorisasi yang lemah
* **Reverse engineering APK** untuk membaca kode sumber, menemukan kerentanan logic, atau informasi sensitif yang tertanam

Dengan melakukan pengujian ini, peserta diharapkan:

* Memahami cara kerja komunikasi antara aplikasi Android dan backend server
* Mengidentifikasi praktik insecure coding yang umum dalam pengembangan aplikasi mobile
* Melatih penggunaan berbagai tools untuk pentest mobile seperti Burp Suite, apktool, dan JADX
* Mendokumentasikan dan mengevaluasi risiko keamanan dari sisi pengguna dan pengembang aplikasi

---

## 3. Tools dan Bahan
- **Tools Utama**:
  - Burp Suite (untuk intercept dan analisis komunikasi aplikasi)
  - Apktool (untuk decompile APK)
  - jadx (untuk reverse engineering kode sumber APK)
  - Android Emulator / Genymotion (untuk menjalankan aplikasi)
  - frida / objection (untuk runtime instrumentation dan bypass SSL pinning)

- **Lab Environment**:
  - Kali Linux (sebagai attacker machine)
  - Android Virtual Device (AVD) atau Genymotion
  - Aplikasi APK InsecureBankv2.apk
  - Java Development Kit (JDK), Android Debug Bridge (ADB)

---

## 4. Metodologi Pengujian
Metode pengujian mengacu pada standar **NIST SP 800-115**:

1. **Planning**
2. **Discovery**
3. **Attack**
4. **Reporting**

---

## 5. Langkah-Langkah Praktikum
https://github.com/dineshshetty/Android-InsecureBankv2

📦 Cara Install Genymotion di Kali Linux:
Download Genymotion .bin file dari situs resmi:

https://www.genymotion.com/download/

Jadikan executable dan jalankan:

bash
Salin
Edit
chmod +x genymotion-*.bin
./genymotion-*.bin
Ini akan mengekstrak dan menginstal Genymotion ke folder baru. Masuk ke folder tersebut:

bash
Salin
Edit
cd genymotion/
./genymotion