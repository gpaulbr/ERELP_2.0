# coding=utf-8

def extracaoCogroo(diretorioTrabalho, categUtilizadas, arquivo, dicFormatado):
	vetorEntrada = list()
	vetorIO = list()
	# dicionario = list()
	# with open ('Profissao_Titulo.txt', encoding="utf8") as dicForm:
	# 	for linha in dicForm.readlines():
	# 		dicionario.append(linha.split(';'))

	# print (dicionario)

	with open(arquivo) as texto:
		features = list()
		
		for linha in texto.readlines():
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
				

				if dic["ID"] in features:

					dic["gerarFeature"] = 'true'
					vetorIO.append("I")

					if dic["lemma"].replace('_', ' ').upper() == "DIRETOR":
						dic["dicionario"] = 'true'

					else: 
						dic["dicionario"] = 'false'

				else:
					dic["gerarFeature"] = 'false'
					dic["dicionario"] = 'false'
					vetorIO.append("O")

				if lista[10][:-1] != '-':

					features = lista[10][1:-2].split('|') 
					dic["gerarFeature"] = 'true'

				vetorEntrada.append(dic)
	file = open('vetorDeEntrada.txt','w')
	file.write(str(vetorEntrada))
	file.close()
	file = open('vetorIO.txt','w')
	file.write(str(vetorIO))
	file.close()
 

categorias = ['PES', 'LOC']
dicionarios = ['./Profissao_Titulo.txt']
extracaoCogroo('./', categorias, 'ric-42664.cg', dicionarios)
