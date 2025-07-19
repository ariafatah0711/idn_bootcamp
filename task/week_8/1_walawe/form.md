# Form Analisis Malware: walawe.exe (Lab01-01.dll)

## 1. Apakah walawe.exe itu virus/malware?
**Ya, berdasarkan hasil analisis, file `walawe.exe` terindikasi kuat sebagai malware (trojan/backdoor).**

---

## 2. Bukti bahwa itu malware
- **Deteksi Multi-Antivirus:**
  - File ini terdeteksi sebagai malware/trojan oleh banyak engine antivirus di VirusTotal (46/72 engine mendeteksi sebagai berbahaya).
- **Label Threat:**
  - Banyak AV memberi label seperti `Trojan.Skeeyah/Doina`, `Win32:Malware-gen`, `Gen:Variant.Doina`, dsb.
- **Hasil ClamAV:**
  - ClamAV juga mendeteksi file ini sebagai `Win.Malware.Agent-6350563-0`.
- **Artefak Statis Mencurigakan:**
  - Ada hardcoded IP address (`127.26.152.13`) yang sering digunakan untuk komunikasi C2 (Command & Control).
  - String mencurigakan seperti `CreateProcessA`, `CreateMutexA`, `exec`, `sleep`, `hello`, dsb.
  - Memanggil API Windows untuk proses dan sinkronisasi.
- **Tidak Menggunakan Proteksi Modern:**
  - NX bit tidak aktif.
  - Symbol tidak di-strip.
- **Screenshot Bukti Deteksi VirusTotal:**
  ![VirusTotal Detection](1_walawe/images/README/image-1.png)

---

## 3. List IOC (Indicators of Compromise) pada walawe.exe
- **File Hashes:**
  - MD5: `290934c61de9176ad682ffdd65f0a669`
  - SHA1: `a4b35de71ca20fe776dc72d12fb2886736f43c22`
  - SHA256: `f50e42c8dfaab649bde0398867e930b86c2a599e8db83b8260393082268f2dba`
- **Static Artifacts:**
  - Hardcoded IP Address: `127.26.152.13`
  - String mencurigakan: `exec`, `CreateProcessA`, `CreateMutexA`, `WS2_32.dll`, `SADFHUHF`, `sleep`, `hello`
- **Metadata:**
  - File Name: `walawe.exe` / `Lab01-01.dll`
  - File Type: Win32 DLL (PE32)
  - Compile Time: 2010-12-19 11:16:38

---

## 4. Tanggal file dikompilasi
- **Compile Time:** 2010-12-19 11:16:38  
  (Diperoleh dari ExifTool, radare2, dan header PE)

---

**Kesimpulan:**
File `walawe.exe` adalah malware/trojan berdasarkan deteksi multi-antivirus, artefak statis, dan perilaku file.  
**Jangan jalankan file ini di sistem normal!**
