with open ('ric-42664.cg') as texto:
	file = open('ric-426642.txt.temp', 'a')
	for line in texto.readlines():
		if line.find('ID_S')!=-1:
			newline = line[:-1] + '\tNE\n'			
		elif line.find('\t')!=-1:
			newline = line[:-1] + '\t-\n'
		file.write(newline)
	file.close()	


