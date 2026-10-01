"""Pengujian sederhana untuk memastikan semua implementasi konsisten."""

import unittest
import subprocess
import sys
from pathlib import Path
from main import SistemAkademik


class TesSistemAkademik(unittest.TestCase):
    def setUp(self):
        self.s = SistemAkademik()

    def tambah_dua(self):
        self.s.tambah_mahasiswa("001", "Fajar", "Informatika")
        self.s.tambah_mahasiswa("002", "Ayu", "Informatika")

    def periksa_sinkron(self):
        nim_list = [x["nim"] for x in self.s.daftar_mahasiswa]
        self.assertEqual(len(nim_list), len(set(nim_list)))
        self.assertEqual(set(nim_list), set(self.s.indeks_mahasiswa))
        for record in self.s.daftar_mahasiswa:
            self.assertIs(record, self.s.indeks_mahasiswa[record["nim"]])

    def test_list_menyimpan_urutan(self):
        self.tambah_dua()
        self.assertEqual([m["nim"] for m in self.s.semua_mahasiswa()], ["001", "002"])
        self.periksa_sinkron()

    def test_cari_key_nim_dan_nim_nol_di_depan(self):
        self.tambah_dua()
        self.assertEqual(self.s.cari_mahasiswa("001")["nama"], "Fajar")
        self.assertIsNone(self.s.cari_mahasiswa("999"))

    def test_menolak_nim_ganda(self):
        self.tambah_dua()
        with self.assertRaises(ValueError):
            self.s.tambah_mahasiswa("001", "Berbeda", "Sains")
        self.assertEqual(len(self.s.daftar_mahasiswa), 2)
        self.periksa_sinkron()

    def test_menolak_input_kosong(self):
        with self.assertRaises(ValueError):
            self.s.tambah_mahasiswa(" ", "Nama", "Informatika")
        with self.assertRaises(ValueError):
            self.s.tambah_mahasiswa("123", "", "Informatika")
        self.periksa_sinkron()

    def test_ubah_sinkron_dan_undo(self):
        self.tambah_dua()
        self.s.ubah_mahasiswa("001", "Fajar Baru", "Teknik Informatika")
        self.assertEqual(self.s.daftar_mahasiswa[0]["nama"], "Fajar Baru")
        self.assertIn("dikembalikan", self.s.undo())
        self.assertEqual(self.s.cari_mahasiswa("001")["nama"], "Fajar")
        self.periksa_sinkron()

    def test_hapus_dan_undo_memulihkan_posisi(self):
        self.tambah_dua()
        self.s.tambah_mahasiswa("003", "Budi", "Informatika")
        self.s.hapus_mahasiswa("002")
        self.assertEqual([m["nim"] for m in self.s.semua_mahasiswa()], ["001", "003"])
        self.assertIsNone(self.s.cari_mahasiswa("002"))
        self.assertIn("dipulihkan", self.s.undo())
        self.assertEqual([m["nim"] for m in self.s.semua_mahasiswa()], ["001", "002", "003"])
        self.periksa_sinkron()

    def test_undo_tambah_menghapus_di_list_dan_dict(self):
        self.tambah_dua()
        self.assertIn("dibatalkan", self.s.undo())
        self.assertEqual([m["nim"] for m in self.s.semua_mahasiswa()], ["001"])
        self.assertIsNone(self.s.cari_mahasiswa("002"))
        self.periksa_sinkron()

    def test_undo_benar_benar_lifo(self):
        self.tambah_dua()
        self.s.ubah_mahasiswa("001", "Fajar Baru", "Informatika")
        self.s.hapus_mahasiswa("002")
        self.s.undo()  # Pulihkan 002
        self.s.undo()  # Pulihkan nama 001
        self.s.undo()  # Batalkan penambahan 002
        self.assertEqual([m["nim"] for m in self.s.semua_mahasiswa()], ["001"])
        self.assertEqual(self.s.cari_mahasiswa("001")["nama"], "Fajar")
        self.periksa_sinkron()

    def test_queue_fifo(self):
        self.tambah_dua()
        self.s.masuk_antrean("002")
        self.s.masuk_antrean("001")
        self.assertEqual(self.s.proses_antrean()[0], "002")
        self.assertEqual(self.s.proses_antrean()[0], "001")
        self.assertIsNone(self.s.proses_antrean())

    def test_queue_menerima_permohonan_berulang(self):
        self.tambah_dua()
        self.s.masuk_antrean("001")
        self.s.masuk_antrean("001")
        self.assertEqual(self.s.lihat_antrean(), ["001", "001"])

    def test_antrean_data_terhapus_dilewati(self):
        self.tambah_dua()
        self.s.masuk_antrean("001")
        self.s.hapus_mahasiswa("001")
        self.assertEqual(self.s.proses_antrean(), ("001", None))
        self.periksa_sinkron()

    def test_antrean_tidak_terdaftar_ditolak(self):
        with self.assertRaises(ValueError):
            self.s.masuk_antrean("999")

    def test_undo_kosong_tanpa_error(self):
        self.assertIn("Tidak ada perubahan", self.s.undo())
        self.assertIsNone(self.s.proses_antrean())

    def test_salinen_bukan_referensi_asli(self):
        self.tambah_dua()
        hasil = self.s.cari_mahasiswa("001")
        hasil["nama"] = "Diubah dari luar"
        hasil_daftar = self.s.semua_mahasiswa()
        hasil_daftar[0]["nama"] = "Diubah lagi"
        self.assertEqual(self.s.cari_mahasiswa("001")["nama"], "Fajar")
        self.periksa_sinkron()

    def test_menu_menangani_input_terputus(self):
        lokasi_program = Path(__file__).resolve().parents[1] / "main.py"
        proses = subprocess.run(
            [sys.executable, str(lokasi_program)],
            input="",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proses.returncode, 0, proses.stderr)
        self.assertIn("Program dihentikan.", proses.stdout)


if __name__ == "__main__":
    unittest.main()
