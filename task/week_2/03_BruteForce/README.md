---

title: Brute-force User Linux dengan Subf
date: 2025-06-08
description: Eksplorasi tool Subf untuk melakukan brute-force user Linux via `su`, menggunakan pendekatan Python dan Bash. Pelajari cara kerja, implementasi, dan potensi dampaknya.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Apa itu Subf?

**Subf** adalah tool buatan sendiri untuk melakukan brute-force terhadap akun user di Linux menggunakan perintah `su`. Tool ini tersedia dalam dua versi: Python dan Bash. Subf akan mencoba berbagai kombinasi password terhadap user tertentu hingga menemukan yang cocok.

![alt text](subf/images/README/image.png)
![alt text](subf/images/README/image-1.png)

Brute-force terhadap `su` biasanya sulit karena sifatnya yang interaktif. Subf mengatasi tantangan ini dengan memanfaatkan modul `pexpect` pada Python dan `expect` pada Bash untuk mengotomatiskan proses tersebut.

Source code tersedia di GitHub: [source code](https://github.com/ariafatah0711/idn_bootcamp/tree/main/task/week_2/03_BruteForce/subf)

---

## Cara Kerja Versi Python

```python
child = pexpect.spawn(f"su {user} -c id", timeout=5)
child.expect("Password:")
child.sendline(password)
index = child.expect([r"(uid=\\d+.+)", "su: Authentication failure", pexpect.EOF, pexpect.TIMEOUT])
```

**Penjelasan singkat:**

* Menggunakan `pexpect` untuk meniru sesi terminal interaktif.
* Saat `su` meminta password, script akan mengirimkan password dari wordlist.
* Jika output mengandung UID, artinya login berhasil.

**Fitur tambahan:**

* Otomatis mendeteksi daftar user dari `/etc/passwd`
* Menampilkan progress brute-force secara real-time
* Mendukung multithread dengan `concurrent.futures` untuk meningkatkan kecepatan

Contoh output ketika password berhasil ditemukan:

```
[SUCCESS] Password ditemukan untuk user 'admin': password123
[RESULT]  uid=1001(admin) gid=1001(admin) groups=1001(admin)
```

---

## Cara Kerja Versi Bash

```bash
expect -c "
    spawn su $USER -c id
    expect {
        \"Password:\" {
            send \"$password\r\"
            expect {
                -re \"uid=.*gid=.*\" { ... }
```

**Penjelasan singkat:**

* Menggunakan `expect` untuk mengotomatiskan input pada perintah `su`
* Lebih ringan, cocok digunakan di server yang tidak memiliki Python

---

## Kenapa Subf Bisa Berhasil?

Perintah `su` menerima input password dari stdin dan merespons melalui stdout, tetapi secara interaktif. Dengan `pexpect` dan `expect`, kita dapat:

* Mendeteksi prompt `Password:`
* Mengirim input password secara otomatis
* Membaca output dan mengevaluasi keberhasilan login

Hal ini tidak semudah dilakukan pada `sudo`, yang umumnya memiliki proteksi `requiretty` untuk mencegah automasi semacam ini.

---

## Cara Menjalankan

### Versi Python:

```bash
python3 subf.py -w wordlist.txt
```

Jika opsi `-u` tidak disertakan, akan muncul daftar user untuk dipilih.

### Versi Bash:

```bash
bash subf.sh wordlist.txt <nama_user>
```

Pastikan Anda memiliki `expect` terinstal di sistem.

---

## Mitigasi dan Etika

> Tool ini hanya ditujukan untuk pembelajaran dan pengujian pada sistem milik sendiri secara legal.

Langkah-langkah mitigasi:

* Gunakan `sudo` dengan konfigurasi `requiretty`
* Batasi user yang boleh menggunakan `su`
* Tambahkan delay saat login gagal menggunakan modul PAM
* Terapkan autentikasi dua faktor (2FA)

---

## Penutup

Subf membuktikan bahwa `su` dapat dieksploitasi secara otomatis dengan pendekatan scripting sederhana. Dari sini kita bisa belajar:

* Bagaimana proses interaktif CLI bekerja di balik layar
* Pentingnya keamanan akun user di Linux
* Kenapa kontrol akses dan audit login itu penting

Gunakan Subf secara bertanggung jawab. Cocok untuk pembelajaran, eksperimen CTF, atau meningkatkan keamanan server pribadi.
