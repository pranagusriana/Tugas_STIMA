FileProcessing = __import__("13519195_FileProcessing")

"""
CLASS DirectedAcyclicGraph : digunakan untuk membuat objek DAG yang direpresentasikan dengan adjacency list dengan bantuan type dictionary
-> Mempunyai atribut:
    - DAG : adjacency list dengan menggunakan dictionary
    - course : array untuk menyimpan course apa saja yang tersedia
    - semester : array untuk menyimpan solusi
    - visited: array untuk menyimpan informasi apakah suatu node telah dikunjungi atau belum
-> Mempunyai method:
    - __init__ : konstruktor untuk membentuk objek
    - buildDAG : membuat directed acyclic graph dari input file
    - delNode : untuk menghapus node dan semua sisi yang keluar dari node tersebut
    - topologiin : untuk mengecek graf yang memiliki derajat masuk = 0 lalu memasukkan ke solusi dan simpul serta sisi yang keluar dari simpul tersebut dihapus dengan delNode
    - topologikeun : untuk mencari solusinya sampai graf DAG kosong
    - printInput : untuk menampilkan persoalan apa yang akan diselesaikan
    - printSolusi : untuk menampilkan solusi yaitu mata kuliah yang dapat diambil setiap semesternya 
-> CATATAN:
    - Input file diasumsikan merupakan DAG (Directed Acyclic Graph) dikarenakan tidak ada penanganan kasus jika inputnya bukan DAG
    - Input file mengikuti aturan: 
        <kode_kuliah_1>,<kode_kuliah_prasyarat_1>,<kode_kuliah_prasyarat2>.
        <kode_kuliah_2>,<kode_kuliah_prasyarat_1>.
        <kode_kuliah_3>.
      Jika tidak maka akan terjadi error
      Semua matkul harus ditulis meskipun tidak memiliki prerequisite untuk menghindari error.
"""

class DirectedAcyclicGraph:
    def __init__(self):
        self.DAG = {}
        self.course = []
        self.semester = [[] for _ in range(8)]
        self.visited = []

    # memiliki parameter berupa string inputFile yang merupakan nama file input yang berada pada folder test
    def buildDAG(self, inputFile):
        fileInput = FileProcessing.readInputFromFile(inputFile)
        i = 0
        while (i < len(fileInput)):
            j = 0
            course = []
            prereq = []
            koma = 0
            strret = ""
            # Memproses input file yang berbentuk <kode_kuliah_1>,<kode_kuliah_prasyarat_1>,<kode_kuliah_prasyarat2>.
            while (j < len(fileInput[i])):
                if (fileInput[i][j] != '.'):
                    if (fileInput[i][j] != ','):
                        strret += fileInput[i][j]
                    else:
                        if (koma > 0):
                            prereq += [strret]
                        else:
                            course += [strret]
                        koma += 1
                        strret = ""
                else:
                    if (koma > 0):
                        prereq += [strret]
                    else:
                        course += [strret]
                j += 1
            # Membuat simpul course dan sisi yang masuk dari prerequisite ke simpul course
            self.DAG[course[0]]=prereq
            i += 1
        for i in self.DAG: # Penambahan semua course yang ada kedalam atribut course
            self.course += [i]

    # Untuk menampilkan DAG, course, dan semester, untuk keperluan debug
    def printGraf(self):
        print(self.DAG, "DAG")
        print(self.course, "COURSE")
        print(self.semester, "SEMESTER")

    # Menerima input parameter berupa node yang akan dihapus
    def delNode(self, node):
        del self.DAG[node] # Hapus simpul
        # Hapus sisi yang keluar dari simpul yang dihapus
        for i in self.DAG:
            temparr = []
            for j in self.DAG[i]:
                if j != node:
                    temparr += [j]
            self.DAG[i] = temparr

    # Mencari solusi (mencari simpul yang derajat masuknya 0 lalu memasukkannya kedalam array semester dengan indeks i)
    # parameter n merupakan indeks dari array course
    # akan terus rekursif sampai n >= banyak course
    def topologiin(self, n, i):
        if (n < len(self.course)):
            if (self.visited[n] == False):
                if (len(self.DAG[self.course[n]]) == 0):
                    self.semester[i] += [self.course[n]]
                    self.visited[n] = True
                    self.topologiin(n+1, i)
                    self.delNode(self.course[n])
                else:
                    self.topologiin(n+1, i)
            else:
                self.topologiin(n+1, i)

    # Mencari solusi (sampai graf DAG kosong)
    def topologikeun(self):
        i = 0
        n = 0
        self.visited = [False for i in range(len(self.course))]
        while (len(self.DAG) != 0):
            self.topologiin(n, i)
            i += 1

    # menampilkan persoalan dari yang berbentuk <kode_kuliah_1>,<kode_kuliah_prasyarat_1>,<kode_kuliah_prasyarat2>.
    # menjadi berbentuk <kode_kuliah_1> <- <kode_kuliah_prasyarat_1> <- <kode_kuliah_prasyarat2>
    def printInput(self, file_output):
        strout = ""
        for i in self.DAG:
            stret = ""
            stret += str(i)
            for j in self.DAG[i]:
                stret += " <- " + j
            strout += stret + "\n"
            print(stret)
        file_output[0] += strout
    
    # Menampilkan solusi yang berupa Semester x : matkul1 matkul2 matkul3
    def printSolusi(self, file_output):
        s = 1
        strout = ""
        for i in self.semester:
            strs = ""
            if (len(i) > 0):
                strs += "Semester " + str(s) + " : "
                for j in i:
                    strs += str(j) + " "
                print(strs)
                strout += strs + "\n"
                s += 1
        file_output[0] += strout

# PRANA GUSRIANA, 13519195, IF2211 STRATEGI ALGORITMA 2021
# SABTU, 27 FEBRUARI 2021 15:50