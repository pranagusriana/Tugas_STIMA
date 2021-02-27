"""
    FUNGSI readInputFromFile menerima parameter namaFile berupa string yang merupakan nama dari file yang akan dibaca
    Filenya terdapat pada folder test
    Input file:
        <kode_kuliah_1>,<kode_kuliah_prasyarat_1>,<kode_kuliah_prasyarat2>.
        <kode_kuliah_2>,<kode_kuliah_prasyarat_1>.
        <kode_kuliah_3>.
    Keluaran dari fungsi ini adalah sebuah array
"""
def readInputFromFile(namaFile):
    file = open("../test/"+namaFile, "r")
    file_input = file.readlines()
    i = 0
    while(i < len(file_input)):
        j = 0
        strRet = ""
        tempstr = file_input[i]
        while (j < len(tempstr)):
            if(tempstr[j] != "\n"):
                strRet += tempstr[j]
            j += 1
        file_input[i] = strRet
        i += 1
    file.close()
    return file_input

"""
    Fungsi saveFile: untuk menyimpan solusi pada file eksternal dengan nama file yaitu namaFile dan isi dari filenya adalah file_output
"""
def saveFile(file_output, namaFile):
    file = open("../test/"+namaFile, "w")
    file.write(file_output)
    file.close()

# PRANA GUSRIANA, 13519195, IF2211 STRATEGI ALGORITMA 2021
# SABTU, 27 FEBRUARI 2021 15:50