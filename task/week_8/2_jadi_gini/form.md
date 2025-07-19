# Form Analisis Malware: Lab01-01.exe (jadi_gini)

## 1. Pada aplikasi jadi gini, apa itu malware?
**Jawaban:**
**Ya**, berdasarkan hasil analisis, file `Lab01-01.exe` pada aplikasi jadi gini terindikasi kuat sebagai malware (trojan/backdoor).

---

## 2. Jika itu malware, apa file tersebut di-obfuscated atau packed? Jika iya, jawab nama packernya.
**Jawaban:**
**Ya**, file ini terindikasi menggunakan packer.
- **Nama packer:** Berdasarkan hasil analisis VirusTotal dan behavior tags, file ini diduga dipacking dengan **Armadillo** (packer).

---

## 3. IoC apa yang ditemukan pada malware tersebut (jika ada)?
**Jawaban:**
**Beberapa Indicators of Compromise (IoC) yang ditemukan:**
- **File Hashes:**
  - MD5: `bb7425b82141a1c0f7d60e5106676bb1`
  - SHA1: `9dce39ac1bd36d877fdb0025ee88fdaff0627cdb`
  - SHA256: `58898bd42c5bd3bf9b1389f0eee5b39cd59180e8370eb9ea838a0b327bd6fe47`
- **Threat Label:**
  - `trojan.ulise/aenjaris`, `Gen:Variant.Ulise`, `Win32:Malware-gen`, dsb.
- **Behavior Tags:**
  - detect-debug-environment, checks-disk-space, long-sleeps, via-tor, armadillo (packer)
- **Vendor Detection:**
  - Terdeteksi oleh 56/72 engine antivirus di VirusTotal.

---

**Kesimpulan:**
File `Lab01-01.exe` pada aplikasi jadi gini adalah malware, terindikasi dipacking dengan Armadillo, dan memiliki beberapa IoC berupa hash, threat label, dan behavior tags. 