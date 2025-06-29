# week 5
- [02_dvwa](./01_dvwa)
- [02_dvapi](./02_dvapi)
- [03_InsecureBankv2](./03_InsecureBankv2/)
- [04_Metasploitable2](./04_Metasploitable2/)

# form
## dvapi
Broken Object Level Authorization (BOLA)
Endpoint tidak memverifikasi kepemilikan objek berdasarkan token.
Dampak: Pengguna dapat mengakses data milik pengguna lain.
Bukti: Output yang menunjukkan akses data user lain tanpa otorisasi.

Broken Authentication
JWT menggunakan secret yang lemah sehingga dapat di-crack dan dimodifikasi.
Dampak: Penyerang bisa mendapatkan akses sebagai admin.
Bukti: Perbandingan output sebelum dan sesudah token dimodifikasi.

Broken Object Property Level Authorization
Tidak ada validasi atribut saat registrasi, sehingga pengguna bisa memanipulasi nilai seperti score.
Dampak: Manipulasi data sensitif oleh pengguna biasa.
Bukti: Output yang menunjukkan nilai score bisa diubah saat registrasi.

## metasploitable
vsftpd 2.3.4 – Backdoor Vulnerability (CVE-2011-2523)
Layanan FTP vsftpd versi 2.3.4 memiliki celah keamanan berupa backdoor yang secara tidak resmi ditambahkan ke dalam source code.
Deskripsi: Jika penyerang melakukan login FTP dengan username yang diakhiri dengan karakter :), maka server akan membuka port backdoor di port 6200. Melalui port ini, penyerang bisa mendapatkan shell root tanpa autentikasi.
Dampak: Remote command execution dengan hak akses root.
Bukti: Eksploitasi menggunakan Metasploit (exploit/unix/ftp/vsftpd_234_backdoor) berhasil memberikan shell root ke sistem target.

## insecurebankv2
Data disimpan tanpa enkripsi di perangkat
Aplikasi menyimpan data sensitif seperti username dan password dalam storage lokal (SharedPreferences) tanpa enkripsi.
Dampak: Data pengguna dapat dengan mudah diekstrak jika perangkat di-root atau disalin file-nya.
Bukti: File .xml pada direktori penyimpanan aplikasi berisi kredensial dalam teks biasa.

## dvwa
Brute Force
Tidak ada limitasi jumlah percobaan login.
Dampak: Penyerang dapat menebak password hingga berhasil login tanpa diblokir.
Bukti: Dapat melakukan login berulang kali tanpa hambatan.

Command Injection
Input dari pengguna tidak disanitasi saat diproses oleh sistem.
Dampak: Penyerang dapat menjalankan perintah shell di server.
Bukti: Perintah seperti ; ls berhasil dieksekusi melalui form.

Cross-Site Request Forgery (CSRF)
Tidak ada implementasi token CSRF dalam permintaan penting.
Dampak: Penyerang bisa membuat user tanpa sadar mengubah data.
Bukti: Permintaan POST bisa dipalsukan dan dijalankan dari situs lain.

Local File Inclusion (LFI)
Parameter page bisa diisi path ke file sistem.
Dampak: Penyerang dapat membaca file sensitif seperti /etc/passwd.
Bukti: File berhasil ditampilkan di halaman web.

File Upload Vulnerability
Tidak ada validasi ekstensi file upload.
Dampak: Penyerang bisa upload script berbahaya dan eksekusi kode jarak jauh (RCE).
Bukti: File .php berhasil diupload dan dijalankan di server.

SQL Injection
Parameter id tidak difilter sebelum digunakan dalam query SQL.
Dampak: Penyerang dapat membaca dan memodifikasi isi database.
Bukti: Query seperti ' OR 1=1-- berhasil digunakan untuk bypass login.

Blind SQL Injection
Variasi dari SQLi tanpa respons langsung dari server.
Dampak: Penyerang tetap bisa mengambil data dengan teknik boolean-based/timing.
Bukti: Respon waktu berbeda tergantung isi query.

DOM-Based XSS
Data dari URL dimanipulasi oleh JavaScript tanpa filter.
Dampak: Penyerang bisa menjalankan script jahat dari URL.
Bukti: Script berbahaya dijalankan dari parameter URL.

Reflected XSS
Input user langsung dirender ke halaman tanpa disanitasi.
Dampak: Penyerang bisa kirim link berisi script berbahaya untuk dijalankan di browser korban.
Bukti: <script>alert(1)</script> langsung dijalankan saat halaman diakses.

Stored XSS
Input disimpan di database dan ditampilkan ke banyak pengguna tanpa validasi.
Dampak: Eksekusi script berbahaya permanen di halaman yang dilihat user lain.
Bukti: Script yang disimpan tetap aktif saat halaman dibuka ulang.