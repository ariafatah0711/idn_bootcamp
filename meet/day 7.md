# scanning
- [docs](https://docs.google.com/presentation/d/1s8RDhuDglfQq2_EkTe8j5tkUtsD7pidjK44oycPIyPo/edit?slide=id.p1#slide=id.p1)

## nmap
### tanpa sudo vs pake sudo
- port scanning nya kalo tanpa sudo full tcp to port sedangkan yang sudo tcp syn to port

### host discovery
- jika P* digunakan maka default akan ditimpa
```bash
-PR = arp scan - host discovery
-PE = icmp echo - host discovery
-PP = icmp timestamp - host discovery
-PS =  TCP syn - host discovery
-PS = TCP ack - host discovery
-PU = UDP - host discovery

-sn = scan without port scanning
```

### port discovery
- jika s* digunakan maka default akan ditimpa
```bash
-sT = tcp 3 way handshake - port discovery
-sS = tcp syn - port discovery
-sU = udp packet - port discovery

-Pn = skip host discovery anggap ip active dan langsung port discovery
```

### more command
```bash
-F = scan 100 most common port
-v = verbose
-vv = very verbose
–reason = make output more reason
-p22,80 = check port 22 and 80
-p1-1023 = check port from 1 to 1023
-p- = check all port
-T0 = slowest scan
-T5 = fastest scan
-r = scan port secara berurutan

--max-rate 50 rate = 50 packets/sec
--min-rate 15 rate = 15 packets/sec
--min-parallelism 100 = 100 probes/ask in parallel

-sV = detect service version
-O = detect operating system
-oA = save output
```

## nmap script
### nmap script engine
- linux =  script disimpan /usr/share/nmap/scripts
- windows = C:\ProgramData\Nmap\scripts

```bash
-sC equivalent --script=default

# single 
nmap --script nama-script <target_ip>

# double
nmap --script nama-script, nama-script <target_ip>

# bulk
nmap --script nama-* <target_ip>
```

### nmap script engine particular category
```bash
auth: Skrip yang terkait dengan otentikasi.
broadcast: Menemukan host di jaringan dengan mengirimkan permintaan siaran.
brute: Melakukan brute-force terhadap layanan.
default (-sC juga memanggil ini): Skrip dasar yang aman dan efisien untuk berbagai tujuan discovery dan deteksi kerentanan umum. Ini adalah kategori yang sering digunakan.
discovery: Menemukan informasi lebih lanjut tentang target.
dos: Menguji kerentanan Denial of Service.
exploit: Skrip eksploitasi dasar.
external: Skrip yang bergantung pada layanan eksternal (misalnya, basis data kerentanan online).
fuzzer: Mengirimkan payload yang tidak valid untuk mencari bug.
intrusive: Skrip yang mungkin noisy atau berpotensi menyebabkan masalah pada target (jangan gunakan di lingkungan produksi tanpa izin!).
malware: Mendeteksi infeksi malware atau backdoor.
safe: Skrip yang tidak akan menyebabkan masalah pada target.
vuln: Skrip untuk mendeteksi kerentanan.

nmap -sV --script vuln <target_ip>
```

## nessus
- Nessus adalah perangkat lunak pemindai kerentanan (vulnerability scanner) yang digunakan untuk mengidentifikasi kelemahan keamanan pada perangkat, aplikasi, sistem operasi, layanan cloud, dan sumber daya jaringan lainnya.

> *untuk cara install & teori silahkan lihat dokumentasi dan modul

