# Sigma Rules & YARA Rules

Dalam lanskap keamanan siber yang berkembang pesat saat ini, mendeteksi dan mengurangi aktivitas berbahaya adalah prioritas utama bagi para profesional keamanan. Dengan meningkatnya volume serangan canggih, penting untuk memanfaatkan alat dan kerangka kerja yang tepat untuk tetap menjadi yang terdepan. Aturan Sigma dan YARA telah muncul sebagai dua kerangka kerja sumber terbuka yang paling kuat dan diadopsi secara luas untuk deteksi ancaman, menawarkan pendekatan standar untuk mengidentifikasi aktivitas berbahaya di berbagai lingkungan. Artikel ini menggali pentingnya kerangka kerja ini, menyoroti bagaimana mereka saling melengkapi untuk menciptakan strategi deteksi yang efektif.

## Memahami Aturan Sigma dan YARA

Deteksi ancaman membutuhkan alat canggih yang mampu mengidentifikasi aktivitas berbahaya di berbagai lingkungan. Aturan Sigma dan YARA telah menjadi bagian integral dari operasi keamanan siber modern. Kerangka kerja sumber terbuka ini memberdayakan analis keamanan untuk mengembangkan metode deteksi standar yang dapat diterapkan lintas platform, meningkatkan kolaborasi antar tim, dan memastikan identifikasi ancaman yang cepat.

Dalam dunia keamanan siber, pertahanan proaktif bukan lagi kemewahan — melainkan kebutuhan. Dua alat yang paling ampuh untuk mengidentifikasi dan menanggapi ancaman adalah aturan Sigma dan YARA. Artikel ini akan memandu Anda dalam menulis aturan Sigma yang efektif untuk deteksi berbasis log serta mengoptimalkan aturan YARA untuk analisis file atau malware — lengkap dengan contoh dan tips praktis.

## Sigma

### Apa itu Sigma?

Sigma adalah format aturan generik dan terbuka yang dirancang untuk mendeskripsikan pola deteksi dalam data log. Diperkenalkan pada tahun 2017, Sigma mirip dengan Snort, namun ditujukan untuk log sistem dibanding lalu lintas jaringan. Sigma memungkinkan tim keamanan menulis aturan deteksi sekali dan mengonversinya ke dalam bahasa kueri SIEM seperti ElasticSearch, Splunk, atau QRadar menggunakan alat seperti `sigmac`. Ini menghilangkan kebutuhan mempelajari bahasa spesifik tiap SIEM.

### Struktur File Sigma (YAML Format)

```yaml
title: Powershell Base64 Command Detection
id: 1234-5678-abcd
status: experimental
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    Image|endswith: powershell.exe
    CommandLine|contains: "-enc"
  condition: selection
level: high
```

Aturan ini mendeteksi proses PowerShell yang menjalankan perintah encoded — metode yang umum digunakan untuk menyembunyikan payload berbahaya.

### Contoh Aturan Sigma Tingkat Lanjut

MITRE ATT\&CK: T1059.001 — PowerShell Execution

```yaml
title: Suspicious Powershell Behavior
id: 2023-05-psh-suspicious
description: Detects potentially malicious PowerShell commands
references:
  - https://attack.mitre.org/techniques/T1059/001/
status: stable
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine|contains:
      - 'Invoke-WebRequest'
      - 'IEX'
      - 'FromBase64String'
  condition: selection
level: critical
tags:
  - attack.execution
  - attack.t1059.001
```

### Elemen Kunci dalam Sigma:

* **title**: Nama aturan
* **logsource**: Kategori log dan produk (misal: Windows)
* **detection**: Pola yang dicari
* **condition**: Kondisi untuk memicu deteksi
* **level**: Tingkat keparahan
* **tags**: Referensi ke MITRE ATT\&CK atau konteks lainnya

### Tools Pendukung:

* `sigmac` (converter CLI untuk SIEM)
* Sigma UI (visual editor)
* Sigma2Rule (tool konversi ke Suricata, OSSEC, dll.)

## YARA

### Apa itu YARA?

YARA (Yet Another Ridiculous Acronym) adalah alat pencocokan pola (pattern-matching) untuk mendeteksi dan mengklasifikasikan malware. Diperkenalkan oleh Victor Alvarez, YARA digunakan oleh analis malware untuk mendeskripsikan karakteristik spesifik malware dalam bentuk aturan.

YARA digunakan untuk:

* Deteksi malware berbasis file dan memori
* Klasifikasi malware ke dalam famili
* Perburuan ancaman (threat hunting)
* Integrasi dengan antivirus atau forensic toolkit

### Struktur YARA Rule:

```c
desciption = "Detects suspicious JavaScript in PDF files"
rule Suspicious_PDF
{
  meta:
    author = "anon"
    description = "Detects suspicious JavaScript in PDF files"
  strings:
    $js = /eval\((.*)\)/
    $stream = /\/JS/
  condition:
    $js and $stream
}
```

Rule ini mendeteksi file PDF yang berisi kode JavaScript mencurigakan — teknik umum dalam eksploitasi dokumen.

### Tips Menulis YARA Rule:

* Gunakan **string yang spesifik** untuk menghindari false positive
* Gabungkan **banyak indikator** untuk presisi
* Gunakan `meta` untuk dokumentasi
* Hindari rule terlalu umum (misal: `eval`, `http`, dsb saja)

### Contoh Aturan YARA Tingkat Lanjut: Cobalt Strike

```c
rule CobaltStrike_Beacon
{
  meta:
    author = "yourname"
    description = "Detects Cobalt Strike beacon payload"
    threat_level = 5
  strings:
    $a = "stageless"
    $b = { 90 90 90 90 90 90 }
    $c = "metasploit"
  condition:
    2 of ($a,$b,$c)
}
```

### Eksekusi Aturan YARA dengan CLI:

Contoh menjalankan aturan YARA terhadap file:

```bash
yara -r cobalt.yar sample.exe
```

Gunakan `-r` untuk recursive scan.

### Penggunaan IOC dalam YARA:

Anda dapat menyisipkan hash, string, offset, signature byte dalam rule untuk mendeteksi file tertentu.

```c
rule IOC_HashMatch
{
  meta:
    description = "Matches known malware hash"
  condition:
    hash.md5 == "44d88612fea8a8f36de82e1278abb02f"
}
```

## IOC (Indicator of Compromise)
### Apa itu IOC

Indicator of Compromise (IOC) adalah artefak digital yang digunakan oleh tim keamanan siber untuk mengidentifikasi potensi pelanggaran keamanan dalam sistem atau jaringan. IOC dapat berupa data teknis yang menandakan adanya aktivitas berbahaya atau serangan, dan sering kali digunakan untuk mendeteksi, merespon, dan mencegah ancaman siber lebih lanjut.

Contoh umum IOC meliputi:

* Alamat IP mencurigakan
* Hash file (MD5, SHA1, SHA256)
* Nama domain atau URL berbahaya
* Nama file atau path tertentu
* String unik dalam kode malware
* Mutex (mutual exclusion object) yang digunakan malware untuk mencegah eksekusi ganda
* Alamat email pengirim phising
* Sertifikat digital mencurigakan

IOC dibagi menjadi tiga kategori utama:

1. **Atomic IOC**: indikator mandiri yang tidak memerlukan konteks (misalnya: IP address, hash).
2. **Computed IOC**: indikator yang memerlukan pemrosesan atau perhitungan (misalnya: hash file).
3. **Behavioral IOC**: indikator berbasis pola perilaku atau aktivitas sistem (misalnya: pembuatan proses tertentu, akses file tertentu).

### IOC yang kamu dapatkan dari malware sebelumnya:

Dari hasil analisis malware sebelumnya, berikut adalah daftar IOC yang ditemukan:

**1. Hash File**

* MD5: `e99a18c428cb38d5f260853678922e03`
* SHA1: `a54d88e06612d820bc3be72877c74f257b561b19`
* SHA256: `9b74c9897bac770ffc029102a200c5de74374f9a95a1c3e0fb9b6e6f3fbb4e48`

**2. IP Address**

* `45.67.23.198` → Diketahui digunakan untuk Command and Control (C2)
* `192.241.203.123` → Server hosting malware

**3. Domain dan URL**

* `malicious-update[.]com`
* `hxxp://evil-site[.]xyz/payload.exe`

**4. Mutex**

* `Global\x1x2x3x4-malware-check`
* `Local\WinMalLock`

**5. String Unik / Artefak Biner**

* `exploit_win32_shellcode_exec`
* `@maldev.core.connect@`

\*\*6. File Path K

## Penutup

Sigma dan YARA bukanlah pesaing — keduanya saling melengkapi. Sigma ideal untuk mendeteksi aktivitas mencurigakan berbasis log, sedangkan YARA unggul dalam analisis dan deteksi file atau memori. Integrasi keduanya dalam pipeline deteksi akan meningkatkan efisiensi dan jangkauan deteksi secara signifikan. Dengan pemahaman dan penerapan yang baik, kedua kerangka kerja ini akan memperkuat pertahanan siber organisasi secara menyeluruh.

## referensi
- [medium.com/@esrakyhn/mastering-sigma-rules-and-yara-rule-optimization-amplify-your-threat-hunting-skills-25d3e102ee83](https://medium.com/@esrakyhn/mastering-sigma-rules-and-yara-rule-optimization-amplify-your-threat-hunting-skills-25d3e102ee83)
- [undercodenews.com/enhancing-cybersecurity-with-sigma-and-yara-rules-a-comprehensive-guide/](https://undercodenews.com/enhancing-cybersecurity-with-sigma-and-yara-rules-a-comprehensive-guide/)