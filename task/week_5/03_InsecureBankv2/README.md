# InsecureBankv2
## 1. Informasi Umum

- **Nama Peserta**        : Aria Fatah
- **Tanggal Praktikum**   : 29 Juni 2025
- **Nama Praktikum**      : API Penetration Testing OWASP API Top 10
- **Target Sistem**       : DVAPI (Damn Vulnerable API)
- **IP/URL Target**       : [http://localhost:3000](http://localhost:3000)

---

## 2. Tujuan Praktikum
Tujuan dari praktikum ini adalah **mengidentifikasi, memahami, dan mengeksploitasi kerentanan umum pada API**, khususnya berdasarkan daftar **OWASP API Security Top 10** seperti **Broken Object Level Authorization (BOLA), Broken Authentication, Excessive Data Exposure, dan lainnya.** Praktikum ini menggunakan DVAPI (Damn Vulnerable API) sebagai target pengujian.

---

## 3. Tools dan Bahan
- **Tools Utama**:
  - Firefox/Chrome DevTools
  - Curl

- **VM/Lab Environment**:
  - DVAPI (Docker container)
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
1. Menjalankan DVAPI menggunakan Docker-Compose: 
   ```bash
   git clone https://github.com/payatu/DVAPI.git
   cd DVAPI
   docker compose up --build
   ```
2. Mengakses aplikasi di browser `http://localhost:3000`
3. register akun, dan login