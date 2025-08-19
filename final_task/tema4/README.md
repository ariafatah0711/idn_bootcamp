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
- T-Pot offers docker images for the following honeypots:<br>
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

## test
- cowrite => ssh
- hellpot => http (bisa pake nginx proxy / apache proxy)
- adbhoney => 5555
- honeyaml => 8080 (buat api auth login)
- wordpot => 8080 wordpress (pake flask)

- miniprint => port 9100 (mini printer)
- mailoney => port 25 (snmp)
- redishoneypot => port 6379 (redis)
- sentrypot => sip port 5060, 8082 (sip)

- conpot => ics/scada (msh gak terlalu paham)
- heralding => honeypot yang berfungsi ngambil cred yang mencoba login ke service tertentu

# testing
