# coding=utf-8


def extracaoCogroo(diretorioTrabalho, categoriasUtilizadas, arquivo, dicFormatado):
    vetorEntrada = list()
    vetorIO = list()
    dicionario = list()

    # Le o arquivo de dicionário e formata ele em um vetor
    with open('Profissao_Titulo.txt') as dicForm:
        for linha in dicForm.readlines():
            dicionario.append(linha[0:linha.find(';')])

    with open(arquivo) as texto:
        features = list()
        gerarFeatureID = None
        gerarFeatureNE = str()

        next(texto)

        for linha in texto:
            dic = dict()

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

                # transforma a string em unicode para o uppercase funcionar nas
                # letras com acento
                lemma = dic["lemma"].decode('utf-8').upper()

                # Substitui os _ por espaços na string e verifica se ela está
                # no dicionário
                if lemma.encode('utf-8').replace('_', ' ') in dicionario:
                    dic["dicionario"] = True

                else:
                    dic["dicionario"] = False

            else:
                dic["dicionario"] = False
                vetorIO.append("O")

            vetorEntrada.append(dic)

            if dic["NE"] in categoriasUtilizadas:

                if gerarFeatureID is None:

                    gerarFeatureID = int(dic["ID"])
                    gerarFeatureNE = dic["NE"]

                else:

                    if dic["NE"] != gerarFeatureNE:

                        diferenca = int(dic["ID"]) - gerarFeatureID

                        for index in range(vetorEntrada.index(dic)-diferenca, vetorEntrada.index(dic)+1):
                            vetorEntrada[index]["gerarFeature"] = True

    file = open('vetorDeEntrada.txt', 'w')
    file.write(str(vetorEntrada))
    file.close()
    file = open('vetorIO.txt', 'w')
    file.write(str(vetorIO))
    file.close()
    for i in vetorEntrada:
        print i

categorias = ['PES', 'ORG', 'LOC']
dicionarios = ['./Profissao_Titulo.txt']
extracaoCogroo('./', categorias, 'ric-42664.cg', dicionarios)
