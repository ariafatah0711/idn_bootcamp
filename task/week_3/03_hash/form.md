# Explain Algorithm Hash
## MD5
MD5 (Message Digest Algorithm 5) adalah algoritma hashing kriptografi yang menghasilkan output sepanjang 128-bit, biasanya dalam bentuk string heksadesimal 32 karakter. Diperkenalkan oleh Ronald Rivest pada tahun 1991, MD5 sempat menjadi standar de facto untuk berbagai kebutuhan hashing karena kecepatan dan efisiensinya. MD5 bekerja dengan memecah data input menjadi blok-blok 512-bit, kemudian memprosesnya menggunakan operasi bitwise dan transformasi matematika kompleks. Hasil akhirnya adalah nilai hash yang tampak acak, namun akan selalu sama untuk input yang identik. Salah satu fitur pentingnya adalah efek avalanche—perubahan sedikit saja pada input akan menghasilkan hash yang sangat berbeda.

Kelebihan utama MD5 adalah kemampuannya menghasilkan hash dengan cepat, serta dukungan luas di berbagai sistem dan bahasa pemrograman. Ini membuatnya cocok untuk aplikasi non-sekuriti seperti checksum file atau validasi integritas data sederhana. Namun, dari sisi keamanan, MD5 kini dianggap tidak lagi layak digunakan. Ini karena kerentanannya terhadap collision—situasi di mana dua input berbeda menghasilkan hash yang sama. Masalah ini sangat krusial dalam konteks tanda tangan digital, verifikasi identitas, dan penyimpanan password, karena dapat dimanfaatkan dalam serangan manipulatif.

Sebagai hasilnya, MD5 sudah tidak direkomendasikan dalam praktik kriptografi modern. Organisasi keamanan dan pengembang sistem disarankan untuk beralih ke algoritma yang lebih aman seperti SHA-256, bcrypt, atau Argon2. MD5 hanya boleh digunakan jika kebutuhan keamanan tidak menjadi prioritas, dan hanya untuk mendeteksi perubahan data atau file dengan tingkat sensitivitas rendah.

## SHA1,SHA256
SHA-1 dan SHA-256 merupakan bagian dari keluarga algoritma SHA (Secure Hash Algorithm) yang dikembangkan oleh NSA dan distandardisasi oleh NIST. Keduanya digunakan untuk menjamin integritas data, namun memiliki tingkat keamanan yang sangat berbeda.

SHA-1 menghasilkan output sepanjang 160-bit dan dulunya banyak digunakan, seperti pada sertifikat SSL dan tanda tangan digital. Namun, sejak awal 2000-an, SHA-1 mulai dianggap tidak aman akibat berkembangnya serangan collision. Pada 2017, serangan praktis terhadap SHA-1 berhasil ditunjukkan secara publik. Karena itu, NIST menyarankan penghentian penggunaan SHA-1 sepenuhnya paling lambat tahun 2030. Saat ini, SHA-1 tidak lagi direkomendasikan untuk digunakan dalam aplikasi keamanan apa pun.

SHA-256, bagian dari keluarga SHA-2, menghasilkan hash sepanjang 256-bit dan menawarkan keamanan yang jauh lebih tinggi. Algoritma ini tahan terhadap serangan collision maupun preimage, menjadikannya standar kriptografi modern yang digunakan secara luas, antara lain dalam:
- Enkripsi data dan sertifikat SSL/TLS
- Teknologi blockchain dan cryptocurrency seperti Bitcoin
- Validasi integritas perangkat lunak (misalnya di sistem Debian)
- Tanda tangan digital dan autentikasi email (seperti DKIM)

Meskipun SHA-256 memerlukan sumber daya komputasi lebih besar dibanding SHA-1, algoritma ini tetap efisien dan mudah diimplementasikan. Oleh karena itu, SHA-256 sangat cocok digunakan untuk aplikasi yang menuntut integritas tinggi dan perlindungan kriptografi yang kuat.

## NTLM Hash
NTLM (NT LAN Manager) adalah protokol autentikasi berbasis challenge-response yang diperkenalkan oleh Windows sejak 1993 sebagai penerus LAN Manager. Meskipun telah tergantikan oleh Kerberos sejak Windows 2000, NTLM masih digunakan untuk keperluan kompatibilitas dengan aplikasi dan perangkat lama. NTLM menyimpan password dalam bentuk hash tanpa salting di database lokal (SAM) atau Active Directory, sehingga hash tersebut setara dengan password dan dapat digunakan untuk autentikasi ulang tanpa perlu mengetahui kata sandi asli.

Terdapat dua versi utama: NTLMv1 menggunakan algoritma lemah seperti MD4 dan LM Hash yang mudah ditembus menggunakan serangan brute-force atau rainbow table, sehingga dinilai sangat rentan. Sementara itu, NTLMv2 menghadirkan perbaikan keamanan dengan menggunakan HMAC-MD5, nonce, dan timestamp, sehingga menghasilkan respons yang berbeda setiap sesi. Namun demikian, NTLMv2 masih memiliki kelemahan karena hash yang dihasilkan tetap bisa digunakan untuk otentikasi, sehingga rentan terhadap serangan pass-the-hash, di mana penyerang cukup mencuri hash untuk mengakses sistem lain. NTLMv2 juga rentan terhadap serangan relay dan man-in-the-middle (MITM), seperti melalui poisoning terhadap protokol LLMNR, NBT-NS, atau SMB, yang memungkinkan penyerang meneruskan hash ke server target.

Akibat kelemahan tersebut, NTLM sering dimanfaatkan dalam serangan lateral movement, di mana satu hash pengguna yang berhasil dicuri bisa digunakan untuk mendapatkan akses penuh ke infrastruktur Active Directory hanya dalam waktu singkat. Karena tingkat risikonya tinggi, Microsoft bahkan telah mengumumkan rencana penghapusan dukungan NTLM secara bertahap antara tahun 2025 hingga 2027.

Untuk meningkatkan keamanan, sangat disarankan untuk menonaktifkan NTLMv1 dan LM Hash, memastikan hanya NTLMv2 yang digunakan dengan aktivasi SMB signing, serta menonaktifkan protokol LLMNR dan NetBIOS yang rawan disalahgunakan. Selain itu, penggunaan Kerberos sebagai mekanisme autentikasi utama, penerapan multi-factor authentication (MFA), pengurangan hak akses administratif, serta aktivasi fitur proteksi seperti Credential Guard, dapat secara signifikan menurunkan risiko pencurian dan penyalahgunaan hash di lingkungan Windows.