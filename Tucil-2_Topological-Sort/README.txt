TUGAS KECIL 2 IF2211 STRATEGI ALGORITMA 2021
" PENYUSUNAN RENCANA KULIAH DENGAN TOPOLOGICAL SORT "

Program yang saya buat bernama "Topologikeun" yaitu sebuah program untuk menyelesaikan persoalan penyusunan rencana kuliah dengan menggunakan topological sort. Program ini dapat menerima input dari file yang berada pada folder test. Jadi jika ingin menambahkan input buat atau ubah file txt yang ada pada folder test lalu memasukkan nama file yang sesuai pada saat program dijalankan (cukup tulis nama file nya saja contoh input.txt). Program ini menyelesaikan persoalan penyusunan rencana kuliah dengan menggunakan pendekatan topological sort.

Pendekatan topological sort yang saya implementasikan adalah buat sebuah DAG dari file inputan, lalu kalau graf belum kosong akan dicek semua simpul yang masih terdapat dalam graf untuk menemukan simpul yang memiliki derajat masuk nol. Lalu simpul yang berderajat masuk nol itu akan dimasukkan kedalam solusi dan dihapus dari graf beserta busur yang keluar dari simpul tersebut. Setelah graf kosong lalu akan ditampilkan solusinya.

CATATAN:
- Input diasumsikan valid (merupakan directed acyclic graph) dan mengikuti aturan penulisan input:
	<kode_kuliah_1>,<kode_kuliah_prasyarat_1>,<kode_kuliah_prasyarat_2>.
	<kode_kuliah_2>,<kode_kuliah_prasyarat_1>.
	<kode_kuliah_3.
- Hanya dapat menerima input matakuliah dalam range 8 semester
- Nama file test case untuk input terdapat pada folder test dengan nama yang diawali input (contoh input8.txt, input.txt). Nama file yang diawali dengan output itu merupakan hasil kompilasi program yang disimpan menjadi file eksternal dan tidak dapat dijadikan input.
- Penjelasan lebih lanjut mengenai setiap fungsi yang dibuat dapat dilihat langsung pada source code yang terdapat pada folder src

REQUIREMENT:
- Minimal menggunakan python versi 3.7.3
- Jika terdapat modul yang belum terinstall silahkan install dengan menggunakan command 
	pip install <nama_modul_yang_belum_terinstall>

Cara menggunakan program:
- Terdapat dua pilihan untuk dapat menggunakan atau menjalankan program. Anda bisa menjalankan program dengan file executable pada folder bin atau dengan file python pada folder src dengan nama filenya adalah 13519195_Main.py
1. Pertama menggunakan file 13519195_Main.py, buka folder ../src/ lalu jalankan command pada command prompt "py 13519195_Main.py"
2. Kedua dengan menggunakan file executable, buka folder ../bin/ lalu double click file 13519195_Main.exe atau pada command promt dapat diketikkan command "13519195_Main.exe"

Author/ Identitas pembuat:
- PRANA GUSRIANA
- 13519195
- K04