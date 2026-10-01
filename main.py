"""Tugas Mandiri 1a - Implementasi struktur data untuk sistem akademik.

Empat kebutuhan utama:
1. List: penyimpanan mahasiswa secara berurutan.
2. Stack: riwayat perubahan untuk Undo (LIFO).
3. Queue: antrean pengolahan data (FIFO) menggunakan deque.
4. Dictionary: pencarian mahasiswa berdasarkan NIM (hash table).

Data hanya tersimpan selama program dijalankan (belum menggunakan database/file).
"""

from collections import deque


class SistemAkademik:
    def __init__(self):
        self.daftar_mahasiswa = []       # List: urutan penambahan mahasiswa
        self.indeks_mahasiswa = {}       # Dict: NIM -> data mahasiswa
        self.riwayat_perubahan = []      # Stack: riwayat tambah, ubah, hapus
        self.antrean = deque()           # Queue: NIM yang akan diproses

    @staticmethod
    def _teks_wajib(nilai, nama_kolom):
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError(f"{nama_kolom} tidak boleh kosong.")
        return nilai.strip()

    def tambah_mahasiswa(self, nim, nama, prodi):
        nim = self._teks_wajib(nim, "NIM")
        nama = self._teks_wajib(nama, "Nama")
        prodi = self._teks_wajib(prodi, "Program studi")
        if nim in self.indeks_mahasiswa:
            raise ValueError("NIM sudah terdaftar; setiap mahasiswa harus memiliki NIM unik.")

        data = {"nim": nim, "nama": nama, "prodi": prodi}
        self.daftar_mahasiswa.append(data)           # LIST: menambah data di akhir
        self.indeks_mahasiswa[nim] = data             # HASH TABLE: indeks menurut NIM
        self.riwayat_perubahan.append(("tambah", nim))  # STACK: simpan tindakan
        return data.copy()

    def semua_mahasiswa(self):
        return [data.copy() for data in self.daftar_mahasiswa]

    def cari_mahasiswa(self, nim):
        nim = self._teks_wajib(nim, "NIM")
        data = self.indeks_mahasiswa.get(nim)         # HASH TABLE: cari berdasarkan key
        return data.copy() if data is not None else None

    def ubah_mahasiswa(self, nim, nama_baru, prodi_baru):
        nim = self._teks_wajib(nim, "NIM")
        nama_baru = self._teks_wajib(nama_baru, "Nama")
        prodi_baru = self._teks_wajib(prodi_baru, "Program studi")
        data = self.indeks_mahasiswa.get(nim)
        if data is None:
            raise ValueError("Mahasiswa dengan NIM tersebut tidak ditemukan.")

        data_sebelum = data.copy()
        # Objek data yang sama dipakai oleh list dan dictionary, jadi keduanya sinkron.
        data["nama"] = nama_baru
        data["prodi"] = prodi_baru
        self.riwayat_perubahan.append(("ubah", nim, data_sebelum))
        return data.copy()

    def hapus_mahasiswa(self, nim):
        nim = self._teks_wajib(nim, "NIM")
        data = self.indeks_mahasiswa.get(nim)
        if data is None:
            raise ValueError("Mahasiswa dengan NIM tersebut tidak ditemukan.")

        # Pencarian posisi dalam List bersifat O(n); jangan mengklaim ini O(1).
        posisi = next(i for i, mhs in enumerate(self.daftar_mahasiswa) if mhs["nim"] == nim)
        data_terhapus = self.daftar_mahasiswa.pop(posisi)
        del self.indeks_mahasiswa[nim]
        self.riwayat_perubahan.append(("hapus", posisi, data_terhapus.copy()))
        return data_terhapus.copy()

    def undo(self):
        if not self.riwayat_perubahan:
            return "Tidak ada perubahan data mahasiswa yang bisa dibatalkan."

        perubahan = self.riwayat_perubahan.pop()      # STACK: LIFO
        jenis = perubahan[0]
        if jenis == "tambah":
            nim = perubahan[1]
            self.daftar_mahasiswa = [m for m in self.daftar_mahasiswa if m["nim"] != nim]
            del self.indeks_mahasiswa[nim]
            return f"Undo berhasil: penambahan mahasiswa {nim} dibatalkan."
        if jenis == "ubah":
            nim, data_sebelum = perubahan[1], perubahan[2]
            self.indeks_mahasiswa[nim].update(data_sebelum)
            return f"Undo berhasil: perubahan mahasiswa {nim} dikembalikan."
        if jenis == "hapus":
            posisi, data_lama = perubahan[1], perubahan[2]
            data_kembali = data_lama.copy()
            self.daftar_mahasiswa.insert(posisi, data_kembali)
            self.indeks_mahasiswa[data_kembali["nim"]] = data_kembali
            return f"Undo berhasil: mahasiswa {data_kembali['nim']} dipulihkan."
        raise RuntimeError("Jenis riwayat perubahan tidak dikenal.")

    def masuk_antrean(self, nim):
        nim = self._teks_wajib(nim, "NIM")
        if nim not in self.indeks_mahasiswa:
            raise ValueError("Mahasiswa harus terdaftar sebelum masuk antrean.")
        self.antrean.append(nim)                    # QUEUE: enqueue di belakang
        return len(self.antrean)

    def lihat_antrean(self):
        return list(self.antrean)

    def proses_antrean(self):
        if not self.antrean:
            return None
        nim = self.antrean.popleft()                 # QUEUE: dequeue dari depan (FIFO)
        # Jika data dihapus sesudah masuk antrean, permintaan dilewati dengan aman.
        return nim, self.cari_mahasiswa(nim)


def cetak_mahasiswa(data):
    print(f"NIM: {data['nim']} | Nama: {data['nama']} | Prodi: {data['prodi']}")


def tampilkan_menu():
    print("\n=== SISTEM ANTRIAN SIDANG SEMINAR (sederhana) ===")
    print("1. Tambah mahasiswa baru")
    print("2. Tampilkan daftar mahasiswa")
    print("3. Ubah data mahasiswa")
    print("4. Hapus data mahasiswa")
    print("5. Undo perubahan ")
    print("6. Tambahkan mahasiswa ke antrean ")
    print("7. Proses antrean ")
    print("8. Lihat antrean")
    print("9. Cari mahasiswa berdasarkan NIM (Dictionary)")
    print("0. Keluar")


def main():
    sistem = SistemAkademik()
    while True:
        tampilkan_menu()
        try:
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "1":
                data = sistem.tambah_mahasiswa(
                    input("NIM: "), input("Nama: "), input("Program studi: ")
                )
                print("Data berhasil ditambahkan:")
                cetak_mahasiswa(data)
            elif pilihan == "2":
                data_semua = sistem.semua_mahasiswa()
                if not data_semua:
                    print("Daftar mahasiswa masih kosong.")
                else:
                    for nomor, data in enumerate(data_semua, start=1):
                        print(f"{nomor}. ", end="")
                        cetak_mahasiswa(data)
            elif pilihan == "3":
                nim = input("NIM yang akan diubah: ")
                data = sistem.ubah_mahasiswa(
                    nim, input("Nama baru: "), input("Program studi baru: ")
                )
                print("Data berhasil diperbarui:")
                cetak_mahasiswa(data)
            elif pilihan == "4":
                data = sistem.hapus_mahasiswa(input("NIM yang akan dihapus: "))
                print(f"Mahasiswa {data['nim']} berhasil dihapus.")
            elif pilihan == "5":
                print(sistem.undo())
            elif pilihan == "6":
                jumlah = sistem.masuk_antrean(input("NIM yang akan diantrekan: "))
                print(f"Berhasil masuk antrean. Jumlah permintaan: {jumlah}.")
            elif pilihan == "7":
                hasil = sistem.proses_antrean()
                if hasil is None:
                    print("Antrean masih kosong.")
                else:
                    nim, data = hasil
                    if data is None:
                        print(f"Permintaan {nim} dilewati: data mahasiswa sudah tidak tersedia.")
                    else:
                        print("Permintaan pertama berhasil diproses:")
                        cetak_mahasiswa(data)
            elif pilihan == "8":
                print("Antrean (depan -> belakang):", sistem.lihat_antrean())
            elif pilihan == "9":
                data = sistem.cari_mahasiswa(input("Masukkan NIM: "))
                if data is None:
                    print("Data mahasiswa tidak ditemukan.")
                else:
                    print("Data ditemukan:")
                    cetak_mahasiswa(data)
            elif pilihan == "0":
                print("Program selesai. Data dalam memori tidak disimpan ke file.")
                break
            else:
                print("Pilihan tidak tersedia. Masukkan angka sesuai menu.")
        except ValueError as error:
            print(f"Input tidak valid: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nProgram dihentikan.")
            break


if __name__ == "__main__":
    main()
