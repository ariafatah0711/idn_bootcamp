# Form Analisis Malware: Lab01-02.bin (wheheh)

## 1. Apa file whehe itu malware?
**Jawaban:**
**Ya**, berdasarkan hasil analisis multi-antivirus (VirusTotal, ClamAV) dan artefak statis, file `Lab01-02.bin` sangat terindikasi sebagai malware (trojan/backdoor).

---

## 2. Kapan aplikasi tersebut di-compile?
**Jawaban:**
- **Tanggal compile:** 2011-01-19 11:10:41 (diperoleh dari ExifTool, field `Time Stamp`)

---

## 3. IoC pada malware, jika ada
**Jawaban:**
Beberapa Indicators of Compromise (IoC) yang ditemukan:
- **File Hashes:**
  - MD5: `8363436878404da0ae3e46991e355b83`
  - SHA1: `5a016facbcb77e2009a01ea5c67b39af209c3fcb`
  - SHA256: `c876a332d7dd8da331cb8eee7ab7bf32752834d4b2b54eaa362674a2a48f64a6`
- **Threat Label:**
  - `Trojan.Skeeyah/Doina`, `Win32:Malware-gen`, `Gen:Variant.Doina`, dsb.
- **Behavior Tags:**
  - pedll, spreader, via-tor, armadillo, checks-user-input
- **Vendor Detection:**
  - Terdeteksi oleh 46/72 engine antivirus di VirusTotal (termasuk ClamAV, Microsoft, BitDefender, dsb).
- **Network IOC:**
  - Hardcoded/contacted IP: `127.26.152.13`

---

**Kesimpulan:**
File `Lab01-02.bin` pada aplikasi wheheh adalah malware, dikompilasi pada 2011-01-19, dan memiliki beberapa IoC berupa hash, threat label, behavior tags, dan network indicator. 