# UBM Racey

## Deskripsi
UBM Racey adalah sebuah game balap sederhana berbasis Python dengan Pygame yang dikontrol menggunakan gerakan kepala. Game ini menggunakan OpenCV dan MediaPipe untuk mendeteksi arah kepala, sehingga pemain dapat mengontrol mobil dalam game hanya dengan menggerakkan kepala ke kiri atau ke kanan.

## Fitur
- **Kontrol menggunakan gerakan kepala** dengan bantuan OpenCV dan MediaPipe
- **Grafik sederhana** menggunakan Pygame
- **Musik dan efek suara** untuk pengalaman bermain yang lebih baik
- **Deteksi tabrakan dan sistem skor** untuk meningkatkan tantangan
- **Tampilan kamera** dalam permainan untuk memonitor pergerakan kepala

## Persyaratan
Sebelum menjalankan game ini, pastikan Anda telah menginstal semua dependensi yang diperlukan:

### 1. Instal Python
Pastikan Python 3 telah terinstal di sistem Anda. Anda dapat mengunduhnya dari [python.org](https://www.python.org/downloads/).

### 2. Instal Pustaka yang Diperlukan
Gunakan pip untuk menginstal pustaka yang dibutuhkan dengan perintah berikut:
```sh
pip install pygame opencv-python mediapipe numpy
```

## Cara Menjalankan
1. Pastikan file **raceDol.png** dan **crash.wav** berada dalam folder yang sama dengan skrip.
2. Jalankan skrip dengan perintah berikut:
```sh
python cam2.py
```
3. Arahkan kepala ke kiri atau kanan untuk mengontrol mobil dalam permainan.

## Kontrol
- **Gerakan kepala kiri** → Mobil bergerak ke kiri
- **Gerakan kepala kanan** → Mobil bergerak ke kanan
- **Tekan 'P'** → Pause permainan
- **Klik tombol 'Quit'** → Keluar dari permainan

## Struktur Kode
- **game_intro()**: Menampilkan layar utama sebelum permainan dimulai.
- **game_loop()**: Loop utama game, mengontrol logika permainan.
- **detect_head_direction()**: Mendeteksi arah gerakan kepala menggunakan MediaPipe.
- **render_camera()**: Menampilkan tampilan kamera dalam permainan.
- **crash()**: Menangani kejadian tabrakan dalam game.

## Catatan
Jika permainan tidak berjalan dengan benar, pastikan kamera Anda berfungsi dengan baik dan pustaka yang dibutuhkan telah terinstal.

## Lisensi
Proyek ini bersifat open-source dan bebas digunakan untuk keperluan pembelajaran.

---
Selamat bermain! 🚗💨

