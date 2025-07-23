# comming soon



---

📚 Yang Harus Dipelajari:
✅ Dasar Sigma Rules
Apa itu Sigma?

Struktur file Sigma (YAML format)

Field penting: logsource, detection, condition, dsb.

Tools: sigmac, Sigma converter ke Elastic, Splunk, dsb.

✅ Dasar YARA Rules
Apa itu YARA dan bagaimana penggunaannya (biasanya untuk scan file/memori).

Struktur YARA rule: meta, strings, condition

Cara menjalankan rule dengan CLI yara

Contoh penggunaan dengan IOC: hash, string, offset, etc.

✅ IOC (Indicator of Compromise)
IOC yang kamu dapatkan dari malware sebelumnya: hash, domain, IP, string unik, mutex, dll.

Mapping IOC ke Sigma (untuk log analysis) dan ke YARA (untuk file/memori scan)

✅ Contoh Use Case
Contoh kasus penggunaan: Deteksi Emotet via registry key access (Sigma), Deteksi malware sample via file hash (YARA)

Kamu bisa buat skenario sederhana: Misalnya malware dropper dengan SHA256 tertentu, lalu cari log proses eksekusinya di eventlog (Sigma), dan buat rule YARA untuk file PE-nya.

✅ Tools
Sigma CLI (sigmac), yara, YARA Python, AnyRun, Hybrid Analysis untuk IOC extraction

