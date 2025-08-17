# dicompot
- [https://github.com/nsmfoo/dicompot](https://github.com/nsmfoo/dicompot)

- port 11112

## teori
dicompot itu honeypot khusus protokol DICOM. Jadi bukan PACS beneran, tapi server “palsu” yang:

> dicompot itu umpan → server DICOM palsu → buat mengamati, mendeteksi, dan menganalisis serangan di lingkungan medis.

### Menipu attacker
Dari luar, dia kelihatan seperti server PACS/DICOM asli (listening di port 104/11112).
Jadi kalau ada attacker scanning rumah sakit / klinik, mereka bisa terkecoh dan nyoba “nyolong” data atau upload file ke server ini.

### Mencatat aktivitas mencurigakan
Semua koneksi (C-ECHO, C-STORE, C-FIND, dsb) direkam.

Kalau ada yang nyoba ngirim DICOM aneh / malicious payload, dicompot akan log detailnya (termasuk metadata pasien palsu yang mereka coba masukkan).

### Tidak menyimpan data medis asli
Karena tujuannya honeypot, dia biasanya cuma balikin respon “palsu” atau status error custom (0x211 kayak yang kamu lihat tadi).
Jadi nggak ada risiko server ini bocorin data pasien asli.

### Alat riset & deteksi serangan
Bisa dipakai di lab buat belajar bagaimana attacker eksploit DICOM.

Bisa dipasang di jaringan rumah sakit buat jadi sensor dini → kalau ada trafik DICOM mencurigakan, kita tahu ada orang scanning/nyoba masuk.

## setup
```bash
git clone https://github.com/nsmfoo/dicompot.git
cd dicompot
docker build -t dicompot:latest .

# net hosts
docker run --rm --read-only --net="host" --name="dicompot" -dit dicompot:latest

# port mapping
docker run --rm --read-only --name="dicompot" -dit -p 11112:11112 dicompot:latest

docker logs dicompot
```

## testing
```bash
# just test
telnet localhost 11112
nc -v localhost 11112
```

### dicom client tools
```bash
sudo apt install dcmtk
echoscu -v localhost 11112

pip install pydicom
cat << EOF > test.py
import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime
from pydicom.uid import generate_uid

filename = "test.dcm"
file_meta = Dataset()
ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

# Required identifiers
ds.PatientName = "Test^Patient"
ds.PatientID = "123456"
ds.Modality = "OT"
ds.StudyInstanceUID = generate_uid()
ds.SeriesInstanceUID = generate_uid()
ds.SOPInstanceUID = generate_uid()
ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.7"  # Secondary Capture Image Storage

# Minimal date/time
ds.ContentDate = datetime.date.today().strftime("%Y%m%d")
ds.ContentTime = datetime.datetime.now().strftime("%H%M%S")

ds.save_as(filename)
print("Created:", filename)
EOF
python3 test.py

storescu -v localhost 11112 test.dcm
```
