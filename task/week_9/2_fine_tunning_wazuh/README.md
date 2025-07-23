# comming soon



---

📚 Yang Harus Dipelajari:
✅ Struktur Rules & Decoder di Wazuh
Decoder: digunakan untuk mengurai format log custom

Rules: mendeteksi pola yang spesifik di log yang sudah didecode

Konsep Atomic ruleset (satu rule untuk satu kondisi)

Konsep Sibling decoder (untuk log kompleks yang berlapis)

✅ Lokasi File
Decoder: /var/ossec/etc/decoders/local_decoder.xml

Rules: /var/ossec/etc/rules/local_rules.xml

✅ Log Format
Pelajari 2 log file yang diberikan (pahami pattern log-nya)

Identifikasi bagian: timestamp, severity, source, message, dst.

✅ Tools & Testing
Cara test log:

Wazuh Dashboard (live test input log)

Gunakan logtest CLI tool: sudo /var/ossec/bin/ossec-logtest

Atau inject log via logstash

Cek hasil: Apakah alert muncul sesuai rule? Apakah decoder bisa parsing dengan benar?

✅ Pelaporan
Buat laporan:

Struktur decoder dan rule

Contoh log input

Hasil output: ID rule, alert description, dan field yang berhasil didecode

Tambahkan ke LinkedIn: Sertakan use case, gambar, atau alert sample

🔸 Tools dan Link yang Direkomendasikan
Kebutuhan	Tools/Link
Sigma Rule Generator	https://uncoder.io/
Sigma Repo	https://github.com/SigmaHQ/sigma
YARA Intro	https://yara.readthedocs.io/en/stable/
Sigma CLI	https://github.com/SigmaHQ/sigmac
IOC Search	https://otx.alienvault.com/, https://www.virustotal.com/
Wazuh Docs	https://documentation.wazuh.com/