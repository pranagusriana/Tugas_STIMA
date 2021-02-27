import DirectedAcyclicGraph
import FileProcesses
import os.path

# PRINT LOGO DARI APLIKASI TOPOLOGIKEUN

print("d888888b  .d88b.  d8888b.  .d88b.  db       .d88b.   d888b  d888888b db   dD d88888b db    db d8b   db")
print("`~~88~~' .8P  Y8. 88  `8D .8P  Y8. 88      .8P  Y8. 88' Y8b   `88'   88 ,8P' 88'     88    88 888o  88")
print("   88    88    88 88oodD' 88    88 88      88    88 88         88    88,8P   88ooooo 88    88 88V8o 88")
print("   88    88    88 88~~~   88    88 88      88    88 88  ooo    88    88`8b   88~~~~~ 88    88 88 V8o88")
print("   88    `8b  d8' 88      `8b  d8' 88booo. `8b  d8' 88. ~8~   .88.   88 `88. 88.     88b  d88 88  V888")
print("   YP     `Y88P'  88       `Y88P'  Y88888P  `Y88P'   Y888P  Y888888P YP   YD Y88888P ~Y8888P' VP   V8P")
print("="*102)
print(" "*9, "Mau milih matkul tapi bingung sama prerequisitenya ???? TOPOLOGIKEUN aja !!!")
print("="*102)
print("")

# INPUT NAMA FILE, JIKA TIDAK TERDAPAT FILE DENGAN NAMA YANG DIINPUTKAN MAKA AKAN DIULANG SAMPAI MENEMUKAN YANG SESUAI
N = input("Masukkan nama file: ")
while (not(os.path.isfile("../test/"+N))):
    print("File tidak ditemukan silahkan masukkan kembali input nama file,")
    N = input("Masukkan nama file: ")

file_output = [""] # INISIALISASI UNTUK KEPERLUAN SAVE FILE (ISI DARI FILE YANG AKAN DISIMPAN)

# INISIALISASI OBJEK DAG
DAG = DirectedAcyclicGraph.DirectedAcyclicGraph()

# MEMBENTUK DAG BERDASARKAN FILE INPUTAN YAITU N
DAG.buildDAG(N)
print("="*30)
print("          Persoalan: ")
print("="*30)
file_output[0] += "="*30 + "\n" + "          Persoalan: \n" + "="*30 + "\n"

# MENAMPILKAN PERSOALAN
DAG.printInput(file_output)

# MENYELESAIKAN PERSOALAN DENGAN MENGGUNAKAN TOPOLOGY SORT
DAG.topologikeun()
print("="*30)
print("           Solusi: ")
print("="*30)
file_output[0] += "="*30 + "\n" + "           Solusi: \n" + "="*30 + "\n"

# MENAMPILKAN SOLUSI DARI PERSOALAN (MATA KULIAH YANG DAPAT DIAMBIL SETIAP SEMESTERNYA)
DAG.printSolusi(file_output)
file_output[0] += "\nBy: Prana Gusriana, 13519195, IF2211 Strategi Algoritma 2021 (TUCIL 2)\n"

# UNTUK MENANYAKAN APAKAH SOLUSINYA AKAN DISIMPAN DI FILE EKSTERNAL
print("="*55)
P = input("Apakah solusi akan disimpan di file eksternal? (Y/N) ")
while (not(P!="Y" or P!="N")):
    print("Maaf hanya menerima input (Y/N), ")
    P = input("Apakah solusi akan disimpan di file eksternal? (Y/N) ")

if (P == "Y"):
    O = input("Masukkan nama file: ")
    while (os.path.isfile("../test/"+O)):
        print("Nama file telah digunakan silahkan masukkan kembali input nama file,")
        O = input("Masukkan nama file: ")
    FileProcesses.saveFile(file_output[0], O) # MENYIMPAN SOLUSI PADA FILE EKSTERNAL
print("="*55)
print("Terimakasih telah menggunakan aplikasi Topologikeun, ^_^")

# PRANA GUSRIANA, 13519195, IF2211 STRATEGI ALGORITMA 2021
# SABTU, 27 FEBRUARI 2021 15:50