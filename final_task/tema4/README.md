## soal
### Implementasi Honeypot untuk Deteksi Dini dan Koleksi Intelijen Ancaman

### Deskripsi Tugas:
Membangun dan menerapkan sistem honeypot yang meniru layanan umum seperti SSH, HTTP, atau ICS untuk menangkap interaksi dari pelaku siber. Sistem ini akan digunakan untuk mengumpulkan indikator serangan secara pasif.

### Hasil yang Diharapkan:
1. Implementasi honeypot seperti Cowrie atau Conpot
2. Sistem pencatatan dan analisis interaksi
3. Laporan hasil klasifikasi perilaku pelaku

---

## Honeypots and Tools
### T-Pot
[adbhoney](https://github.com/huuck/ADBHoney),
[beelzebub](https://github.com/mariocandela/beelzebub),
[ciscoasa](https://github.com/Cymmetria/ciscoasa_honeypot),
[citrixhoneypot](https://github.com/MalwareTech/CitrixHoneypot),
[conpot](http://conpot.org/),
[cowrie](https://github.com/cowrie/cowrie),
[ddospot](https://github.com/aelth/ddospot),
[dicompot](https://github.com/nsmfoo/dicompot),
[dionaea](https://github.com/DinoTools/dionaea),
[elasticpot](https://gitlab.com/bontchev/elasticpot),
[endlessh](https://github.com/skeeto/endlessh),
[galah](https://github.com/0x4D31/galah),
[go-pot](https://github.com/ryanolee/go-pot),
[glutton](https://github.com/mushorg/glutton),
[h0neytr4p](https://github.com/pbssubhash/h0neytr4p),
[hellpot](https://github.com/yunginnanet/HellPot),
[heralding](https://github.com/johnnykv/heralding),
[honeyaml](https://github.com/mmta/honeyaml),
[honeypots](https://github.com/qeeqbox/honeypots),
[honeytrap](https://github.com/armedpot/honeytrap/),
[ipphoney](https://gitlab.com/bontchev/ipphoney),
[log4pot](https://github.com/thomaspatzke/Log4Pot),
[mailoney](https://github.com/awhitehatter/mailoney),
[medpot](https://github.com/schmalle/medpot),
[miniprint](https://github.com/sa7mon/miniprint),
[redishoneypot](https://github.com/cypwnpwnsocute/RedisHoneyPot),
[sentrypeer](https://github.com/SentryPeer/SentryPeer),
[snare](http://mushmush.org/),
[tanner](http://mushmush.org/),
[wordpot](https://github.com/gbrindisi/wordpot)

## tools
### tools fokus ke 1 service
- 1_cowrite → SSH (port 22 default)
- 2_hellpot => HTTP (web, bisa lewat nginx/apache proxy)
- 3_adbhoney => ADB (port 5555)
- 14_honeyaml => HTTP API (auth/login, port 8080)
- 21_wordpot => WordPress emulation (HTTP web app, Flask, port 8080 default)
- 11_h0neytr4p => HTTP/Web (khusus untuk deteksi attacker, bukan sekedar proxy)

### tools yang punya banyak service
- 2_conpot => ICS/SCADA (Modbus, S7, Bacnet, dll)
- 13_heralding => Multi-service credential catcher (SSH, FTP, RDP, dll)
- ddospot => DDoS amplification services (DNS, NTP, SNMP)

### tools yang ke service tapi jarang digunain
- 18_miniprint => Printer service (port 9100, JetDirect)
- 16_mailoney => SMTP (port 25)
- 19_redishoneypot => Redis (port 6379)
- 20_sentrypot => SIP/VoIP (port 5060) + web admin (port 8082)
- 5_ciscoasa => Cisco ASA Firewall (HTTP management interface)
- 9_elasticpot => Elasticsearch (port 9200 default)
- 8_dicompot => DICOM (untuk imaging medis, port 11112/104 default)
- 17_medpot => HL7 / FHIR (untuk sistem medis, port bervariasi)
- 22_snare_tanner => Web honeypot (HTTP frontend + backend)

### tools yang gak terlalu saya pahami
- 4_beelzebub => Multi-service (perlu eksplorasi lebih lanjut)
- 10_go-pot => HTTP/Web service
- 15_honeypots => HTTP/Web service

# testing
