# Host Checker (WebSocket Scanner)

Script Python sederhana untuk memindai daftar host (IP atau domain) secara massal guna mengecek apakah host tersebut merespons koneksi WebSocket (biasanya digunakan untuk mengecek ketersediaan koneksi tunneling seperti Xray, V2Ray, dll).

## Fitur
- **Multithreading:** Cepat karena menggunakan pengecekan paralel (default 15 thread).
- **Deduplikasi Otomatis:** Menghapus host duplikat dari file `list.txt` secara otomatis sebelum dipindai.
- **Status Detail:** Menampilkan respons header HTTP secara langsung, atau menampilkan alasan kegagalan jika host mati (misal: Timeout, SSL/SNI Ditolak, Koneksi Ditolak).
- **Penyimpanan Otomatis:** Hanya host yang berstatus `[LIVE]` (mendapatkan balasan `HTTP/1.1 101 Switching Protocols`) yang akan disimpan ke `result.txt`.
- **Tanpa Dependency:** Hanya menggunakan library bawaan Python (standar), tidak memerlukan `pip install`.

## Cara Penggunaan

1. Pastikan Anda sudah menginstal **Python 3**.
2. Buat file bernama `list.txt` di dalam folder yang sama dengan script (jika belum ada).
3. Masukkan daftar host / IP / Domain yang ingin dicek ke dalam `list.txt` (satu baris untuk satu host).
4. Jalankan script menggunakan perintah:
   ```bash
   python run.py
   ```
5. Host yang berhasil (LIVE) akan tersimpan secara otomatis di dalam file `result.txt`.

## Konfigurasi

Anda dapat mengubah pengaturan koneksi dengan membuka file `run.py` dan menyesuaikan variabel pada bagian **KONFIGURASI** di bagian atas:

```python
# ================= KONFIGURASI =================
SNI = "ray.faridanwar.my.id"         # Server Name Indication
HOST_HEADER = "ray.faridanwar.my.id" # Host header yang dikirim
PATH = "/xray-tunnel"                # Path / Endpoint WebSocket
PORT = 443                           # Port server tujuan (biasanya 443)
TIMEOUT = 5                          # Batas waktu maksimal koneksi (detik)
MAX_THREADS = 15                     # Jumlah proses paralel
# ===============================================
```

## Struktur File
- `run.py`: Script utama.
- `list.txt`: (Tidak dilacak Git) File teks tempat meletakkan daftar host tujuan.
- `result.txt`: (Tidak dilacak Git) File hasil yang mencatat host yang sukses/LIVE.
- `.gitignore`: Konfigurasi agar file data (`list.txt` dan `result.txt`) diabaikan oleh Git.
