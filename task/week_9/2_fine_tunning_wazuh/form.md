# form
## Siblings Decoder, apa itu.. jelaskan dan kirimkan codenya
Sibling decoder merupakan decoder yang berdiri sejajar dengan decoder lain, tanpa hubungan parent-child langsung.

contohnya seperti ini
```bash
<decoder name="nova-api-log-http">
  <parent>nova-api-log</parent>
  ...
</decoder>

<decoder name="nova-api-log-detail">
  <parent>nova-api-log</parent>
  ...
</decoder>
```

Keduanya child dari decoder yang sama, yaitu nova-api-log, tapi tidak bergantung satu sama lain — mereka ini sibling decoder.

## automic ruleset adalah
Atomic ruleset adalah unit terkecil dari rule yang mendeteksi satu event/log spesifik dan tidak tergantung pada event lain. Ini adalah aturan tunggal yang punya syarat sendiri dan langsung memicu alert jika cocok.