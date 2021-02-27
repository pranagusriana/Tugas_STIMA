TUGAS KECIL 2 IF2211 STRATEGI ALGORITMA 2021
" PENYUSUNAN RENCANA KULIAH DENGAN TOPOLOGICAL SORT "

Program yang saya buat bernama "Topologikeun" yaitu sebuah program untuk menyelesaikan persoalan penyusunan rencana kuliah dengan menggunakan topological sort. Program ini dapat menerima input dari file yang berada pada folder test. Jadi jika ingin menambahkan input buat atau ubah file txt yang ada pada folder test lalu memasukkan nama file yang sesuai pada saat program dijalankan (cukup tulis nama file nya saja contoh input.txt). Program ini menyelesaikan persoalan penyusunan rencana kuliah dengan menggunakan pendekatan topological sort.

CATATAN:
- Input diasumsikan valid (merupakan directed acyclic graph) dan mengikuti aturan penulisan input:
	<kode_kuliah_1>,<kode_kuliah_prasyarat_1>,<kode_kuliah_prasyarat_2>.
	<kode_kuliah_2>,<kode_kuliah_prasyarat_1>.
	<kode_kuliah_3.
- Hanya dapat menerima input matakuliah dalam range 8 semester
- Penjelasan lebih lanjut mengenai setiap fungsi yang dibuat dapat dilihat langsung pada source code yang terdapat pada folder src

REQUIREMENT:
- Minimal menggunakan python versi 3.7.3
- Jika terdapat modul yang belum terinstall silahkan install dengan menggunakan command 
	pip install <nama_modul_yang_belum_terinstall>

Cara menggunakan program:
- Terdapat dua pilihan untuk dapat menggunakan atau menjalankan program. Anda bisa menjalankan program dengan file executable pada folder bin atau dengan file python pada folder src dengan nama filenya adalah topologikeun.py
1. Pertama menggunakan file topologikeun,py, buka folder ../src/ lalu jalankan command pada command prompt "py topologikeun.py"
2. Kedua dengan menggunakan file executable, buka folder ../bin/ lalu double click file topologikeun.exe atau pada command promt dapat diketikkan command "topologikeun.exe"

Author/ Identitas pembuat:
- PRANA GUSRIANA
- 13519195
- K04