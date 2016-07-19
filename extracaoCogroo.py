# coding=utf-8

def extracaoCogroo(diretorioTrabalho, categoriasUtilizadas, arquivo, dicFormatado):
	vetorEntrada = list()
	vetorIO = list()
	dicionario = list()
	

	with open ('Profissao_Titulo.txt') as dicForm:				# Le o arquivo de dicionário e formata ele em um vetor
		for linha in dicForm.readlines():						#
			dicionario.append(linha[0:linha.find(';')])			#

	with open(arquivo) as texto:
		features = list()
		gerarFeature = None
		gerarFeatureNE = str()

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
		
					dic["Head"] = True
		
				else:
		
					dic["Head"] = False

				dic["NP"] = (lista[7])
				dic["Structure"] = (lista[8])

				if lista[9] != '-':

					dic["NE"] = (lista[9])
		
				else:

					dic["NE"] = 'null'
				
				if lista[10][:-1] != '-':
					
					features = lista[10][1:-2].split('|') 
				
				dic["gerarFeature"] = False

				if dic["ID"] in features:

					vetorIO.append("I")

					lemma = dic["lemma"].decode('utf-8').upper()			# transforma a string em unicode para o uppercase funcionar nas letras com acento

					if lemma.encode('utf-8').replace('_', ' ') in dicionario:    # Substitui os _ por espaços na string e verifica se ela está no dicionário
						dic["dicionario"] = True

					else: 
						dic["dicionario"] = False

				else:
					dic["dicionario"] = False
					vetorIO.append("O")

				vetorEntrada.append(dic)

				if gerarFeature == None:	
					
					if dic["NE"] in categoriasUtilizadas:
						gerarFeature = int(dic["ID"])
						gerarFeatureNE = dic["NE"]

				if gerarFeature != None:

					if dic["NE"] in categoriasUtilizadas and dic["NE"] != gerarFeatureNE:
						
						diferenca = int(dic["ID"]) - gerarFeature
						
						for index in range(vetorEntrada.index(dic)-diferenca, vetorEntrada.index(dic)+1):
							vetorEntrada[index]["gerarFeature"] = True

	file = open('vetorDeEntrada.txt','w')
	file.write(str(vetorEntrada))
	file.close()
	file = open('vetorIO.txt','w')
	file.write(str(vetorIO))
	file.close()
 

categorias = ['PES', 'ORG']
dicionarios = ['./Profissao_Titulo.txt']
extracaoCogroo('./', categorias, 'ric-42664.cg', dicionarios)
