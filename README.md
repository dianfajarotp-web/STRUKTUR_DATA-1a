# Tugas Mandiri 1a - Struktur Data: Sistem Akademik

Program demonstrasi pengelolaan data mahasiswa untuk empat kebutuhan pada instruksi nomor 4:

| Kebutuhan | Struktur data | Implementasi di `main.py` |
| --- | --- | --- |
| Penyimpanan berurutan | Array dinamis/List | `daftar_mahasiswa` dan `append()` |
| Undo perubahan terakhir | Stack/LIFO | `riwayat_perubahan`, `append()`, `pop()` |
| Antrean pengolahan data | Queue/FIFO | `collections.deque`, `append()`, `popleft()` |
| Cari berdasarkan NIM | Hash Table | `indeks_mahasiswa` (dictionary) dan `.get()` |

Program juga memiliki menu ubah dan hapus untuk mendemonstrasikan Undo pada tiga jenis perubahan (tambah, ubah, hapus).

## Persyaratan dan cara menjalankan

- Python **3.9 atau lebih baru**; tidak memerlukan paket pihak ketiga atau instalasi `pip`.
- Buka terminal di folder proyek lalu jalankan:

```sh
python main.py
```

Pada sebagian komputer, perintah Python dapat berupa `py main.py` atau `python3 main.py`.

## Menu demonstrasi yang disarankan

1. Tambah data NIM `001`, nama `Fajar`, prodi `Informatika`.
2. Tambah NIM `002`, nama `Ayu`, prodi `Informatika`.
3. Tampilkan daftar: urutannya `001` kemudian `002` (List).
4. Cari `002`: ditemukan melalui key NIM (Dictionary).
5. Ubah nama `001`, lalu pilih Undo: nama sebelumnya kembali (Stack).
6. Antrekan `002` dan `001`, lalu proses dua kali: `002` diproses dahulu (Queue).
7. Hapus `002`, lalu Undo: data `002` dipulihkan pada posisi semula (Stack).

## Menjalankan pengujian

```sh
python -m unittest discover -s tests -v
```

## Catatan ketepatan analisis kompleksitas

- Akses posisi `list[i]`: O(1). `list.append()` O(1) **amortisasi**, dan penyisipan/penghapusan di tengah dapat mencapai O(n).
- `riwayat_perubahan.append()` dan `.pop()` adalah operasi Stack, O(1) amortisasi pada List. **Seluruh proses Undo tidak selalu O(1)** karena pemulihan List bisa memerlukan O(n).
- `deque.append()` dan `.popleft()` bekerja O(1) untuk operasi antrean di kedua ujung.
- Akses `dict` dengan key NIM rata-rata O(1), tetapi worst case bisa O(n). Penghapusan data mahasiswa keseluruhan masih mencari posisi pada List (O(n)), walaupun Dictionary menyediakan pencarian key secara rata-rata O(1).
- NIM disimpan sebagai string supaya angka nol di depan tidak hilang.
- Program hanya menyimpan data selama proses berjalan (in-memory); ini adalah demonstrasi struktur data, bukan sistem informasi akademik lengkap.
- Undo hanya membatalkan perubahan **data mahasiswa** (tambah, ubah, hapus). Proses antrean tidak masuk ke riwayat Undo.
- Antrean menyimpan NIM; satu mahasiswa boleh punya lebih dari satu permintaan antrean. Bila data mahasiswa telah dihapus ketika antrean diproses, permintaan itu dilewati dan program tidak crash.

## Referensi resmi

- Python Tutorial, Data Structures: https://docs.python.org/3/tutorial/datastructures.html
- Python `collections.deque`: https://docs.python.org/3/library/collections.html#collections.deque
- Python Wiki, Time Complexity: https://wiki.python.org/moin/TimeComplexity

## Bukti yang disiapkan mahasiswa

- Masukkan proyek ini ke repository GitHub pribadi dan cantumkan URL sebenarnya pada lembar jawaban nomor 9.
- Ambil screenshot kode yang memperlihatkan `daftar_mahasiswa`, `riwayat_perubahan`, `antrean`, `indeks_mahasiswa`, beserta fungsi penggunaan masing-masing untuk nomor 10. Screenshot diambil dari kode yang benar-benar dijalankan.
- Rekam video sesuai ketentuan dosen dan masukkan tautannya pada bagian B.
