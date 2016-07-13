def extracaoCogroo(diretorioTrabalho, categUtilizadas, arquivo, dicFormatado):
	vetor = list()
	
	with open(arquivo) as texto:
		
		for linha in texto.readlines():
			features = list()
			dic = dict()

			if linha[0]!='I':
		
				lista = linha.split('\t')
				dic["ID_S"] = (lista[0])
				dic["ID"] = (lista[1])
		
				if dic["ID"] == 0:
					features = list()

				if lista[3] == '[]':
		
					dic["lemma"] = lista[2]
		
				else:
		
					dic["lemma"] = (lista[3][1:-1])
		
				dic["PoS"] = (lista[4])
		
				if lista[6] == 'O':
		
					dic["Head"] = 'true'
		
				else:
		
					dic["Head"] = 'false'

				dic["NP"] = (lista[7])
				dic["Structure"] = (lista[8])

				if lista[9] != '-':

					dic["NE"] = (lista[9])
		
				else:

					dic["NE"] = 'null'
				
				if lista[10][:-1] != '-':

					features = lista[10][1:-2].split('|') 
				
				if dic["ID"] in features:

					dic["gerarFeature"] = 'true'

					if dic["lemma"].replace('_', ' ') in dicFormatado:
						dic["dicionario"] = 'true'

					else: 
						dic["dicionario"] = 'false'

				else:

					dic["gerarFeature"] = 'false'
					dic["dicionario"] = 'false'

				vetor.append(dic)
	file = open('teste.txt','w')
	file.write(str(vetor))
	file.close()
 


categorias = ['PES', 'LOC']
dicionarios = ['./Dicionarios/Profissao_Titulo.txt']
extracaoCogroo('./', categorias, 'ric-42664.cg', dicionarios)
