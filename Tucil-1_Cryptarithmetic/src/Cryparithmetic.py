import time

class Cryptarithmetic():
	def __init__(self, char, first, currVal):
		self.char = char
		self.first = first
		self.currVal = currVal
		self.query = []
		self.ans = []
		self.posNumber = []
		
	def setQ(self, arrQ):
		self.query += arrQ
		
	def setA(self, arrA):
		self.ans += arrA
		
	def sumQ(self):
		sumq = 0
		for i in range(len(self.query)):
			sumq += self.currVal * (10**self.query[i])
		return sumq
		
	def sumA(self):
		suma = 0
		for i in range(len(self.ans)):
			suma += self.currVal * (10**self.ans[i])
		return suma
		
	def printClass(self):
		print(self.char, self.first, self.currVal, self.query, self.ans)
		
	def setCurrVal(self, integer):
		self.currVal = integer
		
	def setFirst(self, first):
		self.first = first
		
	def setPosNumber(self):
		self.posNumber += [self.currVal]
		
def readInputFromFile(namaFile):
	file = open("../doc/"+namaFile ,"r")
	file_input = file.readlines()
	i = 0
	while(i < len(file_input)):
		j = 0
		strRet = ""
		tempstr = file_input[i]
		while (j < len(tempstr)):
			if (tempstr[j] != "\n"):
				strRet += tempstr[j]
			j += 1
		file_input[i] = strRet
		i += 1
	file.close()
	return file_input
	
def distinguishOpr(query, ans, file_input):
	i = 0
	stop = False
	while(i < len(file_input) and not(stop)):
		if (file_input[i][0] != '-'):
			if (file_input[i][0] != '+'):
				query += [file_input[i]]
			else:
				strRet = ""
				p = 1
				while (p < len(file_input[i])):
					strRet += file_input[i][p]
					p += 1
				query += [strRet]
		else:
			stop = True
		i += 1
	ans += [file_input[i]]
	
def buildArrChar(arrChar, query, ans):
	for i in range(len(query)):
		for j in range(len(query[i])):
			if (j == 0 and len(query[i]) > 1):
				if (arrChar[ord(query[i][j])-65] == 0):
					arrChar[ord(query[i][j])-65] = Cryptarithmetic(query[i][j], True, -1)
				else:
					arrChar[ord(query[i][j])-65].setFirst(True)
			else:
				if (arrChar[ord(query[i][j])-65] == 0):
					arrChar[ord(query[i][j])-65] = Cryptarithmetic(query[i][j], False, -1)
			arrChar[ord(query[i][j])-65].setQ([len(query[i])-j-1])
					
	for i in range(len(ans[0])):
		if (i == 0 and len(ans[0]) > 1):
			if (arrChar[ord(ans[0][i])-65] == 0):
				arrChar[ord(ans[0][i])-65] = Cryptarithmetic(ans[0][i], True, -1)
			else:
				arrChar[ord(ans[0][i])-65].setFirst(True)
		else:
			if (arrChar[ord(ans[0][i])-65] == 0):
				arrChar[ord(ans[0][i])-65] = Cryptarithmetic(ans[0][i], False, -1)
		arrChar[ord(ans[0][i])-65].setA([len(ans[0])-i-1])
		
def sumChar(arrChar):
	sumChr = 0
	for i in range(len(arrChar)):
		if (arrChar[i] != 0):
			sumChr += 1
	return sumChr
	
def cleanFIrstnol(arrChar):
	idxFirst = []
	idx = 0
	idxAr = []
	for i in range(len(arrChar)):
		if (arrChar[i] != 0):
			if (arrChar[i].first == True):
				idxFirst += [i]
				idxAr += [idx]
			idx += 1
	arr = []
	lenPos = len(arrChar[idxFirst[0]].posNumber)
	for i in range(lenPos):
		tempArr = []
		for j in range(len(arrChar)):
			if (arrChar[j] != 0):
				tempArr += [arrChar[j].posNumber[i]]
		arr += [tempArr]

	for i in range(len(idxFirst)):
		col = idxAr[i]
		tempSol =[]
		for j in range(len(arr)):
			if (arr[j][col]!=0):
				tempSol += [arr[j]]
		arr = tempSol
		
	for j in range(len(arrChar)):
		if (arrChar[j] != 0):
			arrChar[j].posNumber = []
			
	for i in range(len(arr)):
		p = 0
		for j in range(len(arrChar)):
			if (arrChar[j] != 0):
				arrChar[j].posNumber += [arr[i][p]]
				p+=1
				
def printHasil(arrChar, query, ans, file_input, file_output):
	file_outputt = ""
	for i in file_input:
		print(i)
		file_outputt += i + "\n"
	arrSol = []
	arrOut = []
	sumSol = 0
	totChar = sumChar(arrChar)
	p = 0
	stopS = False
	while (p < len(arrChar) and not(stopS)):
		if (arrChar[p] != 0):
			sumSol = len(arrChar[p].posNumber)
			stopS = True
		else:
			p+=1
	if (sumSol != 0):
		print("====================================================================================================\n" + "                  Terdapat " + str(sumSol) + " Solusi dari permainan cryptarithmetic ini, yaitu: " + "\n====================================================================================================")
		file_outputt += "====================================================================================================\n" + "                  Terdapat " + str(sumSol) + " Solusi dari permainan cryptarithmetic ini, yaitu: " + "\n====================================================================================================\n"
		for i in range(sumSol):
			Sol = ""
			idxChar = 0
			for j in range(len(arrChar)):
				if (arrChar[j] != 0):
					Sol += ( str(arrChar[j].char) + " = " + str(arrChar[j].posNumber[i] ) )
					if (idxChar < totChar - 1):
						if (idxChar == totChar -2):
							Sol += ", dan "
						else:
							Sol += ", "
					idxChar += 1
			arrSol += [Sol]
			tempArrout = []
			for p in range(len(query)):
				subsChar = ""
				for q in range(len(query[p])):
					subsChar += str(arrChar[ord(query[p][q])-65].posNumber[i])
				if (p != len(query)-1):
					tempArrout += [subsChar]
				else:
					tempArrout += [subsChar + " +"]
			tempArrout += ["----------"]
			tempans = ""
			for s in range(len(ans[0])):
				tempans += str(arrChar[ord(ans[0][s])-65].posNumber[i])
			tempArrout += [tempans]
			arrOut += [tempArrout]
		
		for i in range(sumSol):
				print("==================== Solusi ke-[" + str(i+1) + "] : " + arrSol[i] + " ====================")
				file_outputt += "==================== Solusi ke-[" + str(i+1) + "] : " + arrSol[i] + " ====================\n"
				for j in range(len(arrOut[i])):
					print(arrOut[i][j])
					file_outputt += arrOut[i][j] + "\n"
				print("")
				file_outputt += "\n"
	else:
		print("Tidak memiliki solusi")
		file_outputt += "Tidak memiliki solusi\n"
	file_output += [file_outputt]
		
def updatePosNumber(arr, arrChar, query, ans):
	idx = 0
	i = 0
	while(i < len(query)):
		if (arrChar[ord(query[i][0])-65].currVal == -1 and len(query[i]) > 1):
			arrChar[ord(query[i][0])-65].setCurrVal(arr[idx])
			idx += 1
		i += 1
	if (arrChar[ord(ans[0][0])-65].currVal == -1 and len(ans[0]) > 1):
		arrChar[ord(ans[0][0])-65].setCurrVal(arr[idx])
		idx += 1
	j = 0
	while (j < len(arrChar)):
		if (arrChar[j] != 0):
			#print(idx, arrChar, arr)
			if (arrChar[j].first == False):
				arrChar[j].currVal = arr[idx]
				idx += 1
		j += 1
	
	sumq = 0
	suma = 0
	for i in range(len(arrChar)):
		if (arrChar[i] != 0):
			sumq += arrChar[i].sumQ()
			suma += arrChar[i].sumA()
	if (sumq == suma):
		for i in range(len(arrChar)):
			if (arrChar[i] != 0):
				arrChar[i].setPosNumber()
				arrChar[i].setCurrVal(-1)
	else:
		for i in range(len(arrChar)):
			if (arrChar[i] != 0):
				arrChar[i].setCurrVal(-1)
				
def isFirstExist(arrChar):
        First = 0
        for i in range(len(arrChar)):
                if (arrChar[i] != 0):
                        if (arrChar[i].first == True):
                                First += 1
        if (First == 0):
                return False
        else:
                return True

def Solve(arrChar, query, ans, file_input, file_output, tes):
	totalChar = sumChar(arrChar)
	
	if (totalChar == 10):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							for fourth in range (10):
								if (fourth != first and fourth != scnd and fourth != thrd):
									for fifth in range (10):
										if (fifth != first and fifth != scnd and fifth != thrd and fifth != fourth):
											for sixth in range(10):
												if (sixth != first and sixth != scnd and sixth != thrd and sixth != fourth and sixth != fifth):
													for seventh in range(10):
														if (seventh != first and seventh != scnd and seventh != thrd and seventh != fourth and seventh != fifth and seventh != sixth):
															for eighth in range(10):
																if (eighth != first and eighth != scnd and eighth != thrd and eighth != fourth and eighth != fifth and eighth != sixth and eighth != seventh):
																	for nineth in range(10):
																		if (nineth != first and nineth != scnd and nineth != thrd and nineth != fourth and nineth != fifth and nineth != sixth and nineth != seventh and nineth != eighth):
																			for tenth in range(10):
																				if (tenth != first and tenth != scnd and tenth != thrd and tenth != fourth and tenth != fifth and tenth != sixth and tenth != seventh and tenth != eighth and tenth != nineth):
																					arr = [first, scnd, thrd, fourth, fifth, sixth, seventh, eighth, nineth, tenth]
																					updatePosNumber(arr, arrChar, query, ans)
																					tes[0] += 1
	elif (totalChar==9):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							for fourth in range (10):
								if (fourth != first and fourth != scnd and fourth != thrd):
									for fifth in range (10):
										if (fifth != first and fifth != scnd and fifth != thrd and fifth != fourth):
											for sixth in range(10):
												if (sixth != first and sixth != scnd and sixth != thrd and sixth != fourth and sixth != fifth):
													for seventh in range(10):
														if (seventh != first and seventh != scnd and seventh != thrd and seventh != fourth and seventh != fifth and seventh != sixth):
															for eighth in range(10):
																if (eighth != first and eighth != scnd and eighth != thrd and eighth != fourth and eighth != fifth and eighth != sixth and eighth != seventh):
																	for nineth in range(10):
																		if (nineth != first and nineth != scnd and nineth != thrd and nineth != fourth and nineth != fifth and nineth != sixth and nineth != seventh and nineth != eighth):
																			arr = [first, scnd, thrd, fourth, fifth, sixth, seventh, eighth, nineth]
																			updatePosNumber(arr, arrChar, query, ans)
																			tes[0] += 1
	elif (totalChar==8):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							for fourth in range (10):
								if (fourth != first and fourth != scnd and fourth != thrd):
									for fifth in range (10):
										if (fifth != first and fifth != scnd and fifth != thrd and fifth != fourth):
											for sixth in range(10):
												if (sixth != first and sixth != scnd and sixth != thrd and sixth != fourth and sixth != fifth):
													for seventh in range(10):
														if (seventh != first and seventh != scnd and seventh != thrd and seventh != fourth and seventh != fifth and seventh != sixth):
															for eighth in range(10):
																if (eighth != first and eighth != scnd and eighth != thrd and eighth != fourth and eighth != fifth and eighth != sixth and eighth != seventh):
																	arr = [first, scnd, thrd, fourth, fifth, sixth, seventh, eighth]
																	updatePosNumber(arr, arrChar, query, ans)
																	tes[0] += 1
	elif (totalChar==7):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							for fourth in range (10):
								if (fourth != first and fourth != scnd and fourth != thrd):
									for fifth in range (10):
										if (fifth != first and fifth != scnd and fifth != thrd and fifth != fourth):
											for sixth in range(10):
												if (sixth != first and sixth != scnd and sixth != thrd and sixth != fourth and sixth != fifth):
													for seventh in range(10):
														if (seventh != first and seventh != scnd and seventh != thrd and seventh != fourth and seventh != fifth and seventh != sixth):
															arr = [first, scnd, thrd, fourth, fifth, sixth, seventh]
															updatePosNumber(arr, arrChar, query, ans)
															tes[0] += 1
	elif (totalChar==6):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							for fourth in range (10):
								if (fourth != first and fourth != scnd and fourth != thrd):
									for fifth in range (10):
										if (fifth != first and fifth != scnd and fifth != thrd and fifth != fourth):
											for sixth in range(10):
												if (sixth != first and sixth != scnd and sixth != thrd and sixth != fourth and sixth != fifth):
													arr = [first, scnd, thrd, fourth, fifth, sixth]
													updatePosNumber(arr, arrChar, query, ans)
													tes[0] += 1
	elif (totalChar==5):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							for fourth in range (10):
								if (fourth != first and fourth != scnd and fourth != thrd):
									for fifth in range (10):
										if (fifth != first and fifth != scnd and fifth != thrd and fifth != fourth):
											arr = [first, scnd, thrd, fourth, fifth]
											updatePosNumber(arr, arrChar, query, ans)
											tes[0] += 1
	elif (totalChar==4):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							for fourth in range (10):
								if (fourth != first and fourth != scnd and fourth != thrd):
									arr = [first, scnd, thrd, fourth]
									updatePosNumber(arr, arrChar, query, ans)
									tes[0] += 1
	
	elif (totalChar==3):
		#print("hallo")
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					for thrd in range(10):
						if (thrd != first and thrd != scnd):
							arr = [first, scnd, thrd]
							updatePosNumber(arr, arrChar, query, ans)
							tes[0] += 1
	elif (totalChar==2):
		for first in range(10):
			for scnd in range(10):
				if (scnd!=first):
					arr = [first, scnd]
					updatePosNumber(arr, arrChar, query, ans)
					tes[0] += 1
	elif (totalChar==1):
		for first in range(10):
			arr = [first]
			updatePosNumber(arr, arrChar, query, ans)
			tes[0] += 1
	else:
		file_outputt = ""
		for i in file_input:
			print(i)
			file_outputt += i + "\n"
		print("====================================================================================================\n         Maaf jumlah total huruf masukkannya lebih dari 10 huruf, tidak bisa diselesaikan :)\n====================================================================================================\n")
		file_outputt += "====================================================================================================\n         Maaf jumlah total huruf masukkannya lebih dari 10 huruf, tidak bisa diselesaikan :)\n====================================================================================================\n"
		file_output += [file_outputt]
	if (1<= totalChar <= 10):
		if (isFirstExist(arrChar)):
			cleanFIrstnol(arrChar)					
		printHasil(arrChar, query, ans, file_input, file_output)

def saveFile(file_output, namaFile):
	file = open("../doc/"+namaFile, "w")
	file.write(file_output)
	file.close()
	
			
def Main():		
	arrChar = [0 for i in range(26)]					
	file_input = readInputFromFile("input9.txt")
	query = []
	ans = []
	file_output = []
	tes = [0]
	distinguishOpr(query, ans, file_input)
	buildArrChar(arrChar, query, ans)
	start_time = time.time()
	Solve(arrChar, query, ans, file_input, file_output, tes)
	print("====================================================================================================")
	print("----------------------------- %s seconds -----------------------------" %(time.time() - start_time))
	print("----------------------------- "+ str(tes[0]) + " total test -----------------------------")
	file_output[0] += "====================================================================================================\n" +  "----------------------------- %s seconds -----------------------------\n" %(time.time() - start_time) + "----------------------------- "+ str(tes[0]) + " total test -----------------------------\n"
	saveFile(file_output[0], "output9.txt")
	
Main()
