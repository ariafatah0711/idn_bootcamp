# resource
- [drive](https://drive.google.com/drive/folders/1Hh-BMcLIpk4VWB5mfMOj_sK84zmqpl_w?usp=sharing)

## A. tema 1
### Pengembangan Platform Simulasi Adversarial Berbasis MITRE ATT&CK

### tools
- [atomicredteam](https://www.atomicredteam.io/)
- [mitre/caldera](https://github.com/mitre/caldera)
- [guardicore/monkey](https://github.com/guardicore/monkey)

### Simulasi Adversarial → Serangan Hacker
Simulasi → Serangan Hacker → Mitre ATT&CK → AI( Data Real Keagle )  → Dashboard → Hypotest → Threat Hunting

### Deskripsi Tugas:
Merancang dan membangun platform simulasi serangan siber yang mengikuti skenario berbasis taktik dan teknik dari MITRE ATT&CK. Platform ini diharapkan dapat digunakan untuk menguji efektivitas sistem pertahanan siber secara sistematis.

### Hasil yang Diharapkan:
1. Sistem berbasis CLI atau web yang dapat menjalankan rangkaian serangan (kill chain)
   - Caldera & Infected Monkey & Invoke Automic
     - Caldera → Melakukan Procedure Nmap → Sofware OS
2. Dokumentasi pemetaan teknik ke MITRE ATT&CK
   - 1 Teknik ( T1592.002 Host Discover Software )
     - Catat → Procedure → Syntax Hacker ( nmap -sV → Software Version , Log Php /phpinfo.php → Software, etc ..
     - Hacker bisa dapetin informasi software dengan melakukan nmap seperti ```nmap -sV IP```
   - Kill Chain ( APT29 )
     - Persistenc e
       - Cron Job: Syntax, How To Detect, Remedetaion, Saran
     - Publik Key Abuse
     - ADS → Steganoe
   - Intial Access
     - https://mitre-attack.github.io/attack-navigator//#layerURL=https%3A%2F%2Fattack.mitre.org%2Fgroups%2FG0016%2FG0016-enterprise-layer.json
3. Demonstrasi pengujian terhadap log pertahanan ( Rules & Decoder )
   - Wazuh
     - Rules & Decoder
       - Mitre Taktik & Teknik
   - Yara Sigma

- → Mereka Butuh Pengimplentasian Teknik & Taktik MITRE ATT&CK → Threat Modeling → Risk yang ada di kantor → Berdasarakan Taktik & Teknik Yang sudah. → Remedetion Threat Modeling
- Proxmox
  - Agent -> Windows / Linux
  - Wazuh -> All In One
- Coba install tools !!
  - Caldera
  - Invokede
- Execution si caldera / invoked
  - Invoke-testRedtead →
- Minotiring -> Terdeteksi atau tidak
- Rmediaton → Report

---

## B. tema 2
### Perancangan Framework Command and Control (C2) dengan Teknik Evasion

### Deskripsi Tugas:
Membangun framework C2 modular yang dirancang untuk menghindari deteksi oleh sistem IDS/EDR. Penekanan diberikan pada teknik pengaburan (evasion) seperti domain fronting, JA3 evasion, dan jittering.

### Hasil yang Diharapkan:
1. Implementasi server dan agen C2 yang dapat dikustomisasi
2. Uji coba komunikasi tersembunyi terhadap Suricata/IDS
   - Crafting Packet Scapy
     - Python Script → Abuse Firewall Rules → FireWallking
3. Analisis lalu lintas jaringan dan dokumentasi evasion

---

## C. tema 3
Pengembangan Sistem Deteksi Intrusi Berbasis Anomali untuk Suricata

### Deskripsi Tugas:
Mengembangkan modul deteksi berbasis perilaku (anomali) sebagai pelengkap sistem IDS Suricata yang berbasis signature. Sistem harus mampu membedakan aktivitas normal dan anomali pada trafik jaringan

### Hasil yang Diharapkan:
1. Sistem pemantauan anomali berbasis Python/ML sederhana
2. Dataset dan baseline trafik normal
3. Studi kasus dan hasil deteksi terhadap pola serangan

---

## D. tema 4
### Implementasi Honeypot untuk Deteksi Dini dan Koleksi Intelijen Ancaman

### Deskripsi Tugas:
Membangun dan menerapkan sistem honeypot yang meniru layanan umum seperti SSH, HTTP, atau ICS untuk menangkap interaksi dari pelaku siber. Sistem ini akan digunakan untuk mengumpulkan indikator serangan secara pasif.

### Hasil yang Diharapkan:
1. Implementasi honeypot seperti Cowrie atau Conpot
2. Sistem pencatatan dan analisis interaksi
3. Laporan hasil klasifikasi perilaku pelaku

---

## E. tema 5
### Pengembangan Perangkat Otomatisasi Threat Hunting dengan Sigma Rule

### Deskripsi Tugas:
Mendesain perangkat lunak yang dapat melakukan threat hunting secara otomatis dengan menggunakan log dari sistem (Sysmon/ELK) dan menerapkan rule berbasis Sigma yang telah dipetakan ke MITRE ATT&CK.

### Hasil yang Diharapkan:
1. Integrasi rule Sigma dengan log parser
2. Dokumentasi hasil pencarian IOC/TTP
3. Studi penggunaan di lingkungan simulasi

---

## F. tema 6
### Otomatisasi Pengujian Keamanan Aplikasi Mobile Berbasis OWASP MSTG

### Deskripsi Tugas:
Mengembangkan perangkat analisis statis dan dinamis terhadap aplikasi Android yang memeriksa kelemahan seperti insecure data storage, komunikasi tidak terenkripsi, dan kelemahan logika bisnis.

### Hasil yang Diharapkan:
1. Tools analisis APK dengan Androguard dan Frida
2. Panduan pemetaan hasil ke OWASP MSTG
3. Dokumentasi studi kasus pada aplikasi uji coba

---

## G. tema 7
### Rancang Bangun Sistem Audit Keamanan untuk Infrastructure-as-Code dan Container

### Resource:
- [dependabot](https://github.com/dependabot)
- [synk.io](https://snyk.io/)

### Deskripsi Tugas:
Membuat sistem otomatisasi audit terhadap konfigurasi Dockerfile, Kubernetes manifest, dan skrip Terraform guna mendeteksi kesalahan konfigurasi yang rentan terhadap eksploitasi.

### Hasil yang Diharapkan:
1. Sistem audit CLI berbasis Python/Bash
2. Laporan hasil pemeriksaan terhadap benchmark CIS
3. Studi kasus konfigurasi tidak aman yang berhasil diidentifikasi

## H. tema 8
### Pengembangan Alat Deteksi Ancaman pada Active Directory Berbasis Log Event

### Deskripsi Tugas:
Membangun sistem untuk mendeteksi upaya kompromi terhadap Active Directory, seperti Kerberoasting dan DCSync, melalui analisis terhadap log Event ID dan konfigurasi direktori.

### Hasil yang Diharapkan:
1. Parser log dan alert generator berbasis PowerShell/Python
2. Simulasi teknik serangan dan laporan deteksi
3. Studi efektivitas dalam lingkungan lab AD

---

## I. tema 9
### Pembuatan Sistem Deteksi Anomali untuk Jaringan ICS/SCADA

### Deskripsi Tugas:
Merancang sistem pemantauan trafik Modbus/TCP dan protokol industri lainnya, untuk mengidentifikasi perilaku tidak biasa pada jaringan kontrol industri (OT).

### Hasil yang Diharapkan:
1. Sniffer protokol ICS dan sistem pelabelan anomali
2. Hasil baseline dan deteksi terhadap trafik manipulatif
3. Analisis dan visualisasi pola komunikasi

---

## J. tema 10
### Implementasi Honeypot ICS untuk Studi Perilaku Penyerang Terhadap OT

### Deskripsi Tugas:
Menerapkan honeypot ICS dengan skenario simulasi perangkat industri, yang memungkinkan pengumpulan data serangan terhadap sistem kontrol seperti HMI, PLC, dan RTU.

### Hasil yang Diharapkan:
1. Konfigurasi honeypot ICS menggunakan Conpot atau GridPot
2. Laporan interaksi yang dicatat dari penyerang
3. Studi kasus dan klasifikasi TTP yang digunakan

## K. tema 11
### Pengembangan Framework Pengujian Keamanan Aplikasi Web dengan Fokus pada Akses dan Logika

### Deskripsi Tugas:
Merancang sistem pengujian keamanan aplikasi web secara otomatis yang mampu mendeteksi kelemahan kontrol akses dan logika bisnis, termasuk IDOR dan privilege escalation.

### Hasil yang Diharapkan:
1. Framework crawler dan pemetaan peran pengguna
2. Laporan uji akses dengan perbandingan hasil response
3. Studi pada aplikasi uji coba dengan user multi-role

## L. tema 12
### Pembuatan Sistem Sandbox (VM Flare ) untuk Analisis Perilaku Malware

### Deskripsi Tugas:
Membangun sistem eksekusi file mencurigakan dalam lingkungan sandbox terisolasi untuk mencatat perubahan pada sistem, jaringan, registry, dan mendeteksi karakteristik berbahaya secara perilaku.

### Hasil yang Diharapkan:
1. Virtualisasi sistem sandbox berbasis Proxmox/VM
2. Integrasi Sysmon dan YARA untuk klasifikasi aktivitas
3. Laporan hasil analisis terhadap contoh malware
