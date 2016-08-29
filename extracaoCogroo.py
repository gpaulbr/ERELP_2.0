# coding=utf-8

import os


def extracaoCogroo(diretorioTrabalho, categoriasUtilizadas, arquivo, vetDicionarios):
    vetorEntrada = list()
    vetorIO = list()
    # Dicionario com as palavras dos arquivos de dicionarios passados para o método
    dic = dict()
    numeroRelacoes = 0

    # Le os txts de dicionarios e formata eles no dic
    for dicionario in vetDicionarios:
        with open(dicionario) as dicForm:
            for linha in dicForm.readlines():
                dic[(linha[0:linha.find(';')])] = True

    with open(arquivo) as texto:
        vetorRel = list()
        gerarFeatureID = None
        gerarFeatureNE = str()

        next(texto)

        for linha in texto:

            dicPalavra = dict()

            lista = linha.split('\t')
            dicPalavra["ID_S"] = (lista[0])
            dicPalavra["ID"] = (lista[1])

            if dicPalavra["ID"] == 0:
                vetorRel = list()

            if lista[3] == '[]':

                dicPalavra["lemma"] = lista[2]

            else:

                dicPalavra["lemma"] = (lista[3][1:-1])

            dicPalavra["PoS"] = (lista[4])

            if lista[6] == 'O':

                dicPalavra["Head"] = True

            else:

                dicPalavra["Head"] = False

            dicPalavra["NP"] = (lista[7])
            dicPalavra["Structure"] = (lista[8])

            if lista[9] != '-':

                dicPalavra["NE"] = (lista[9])

            else:

                dicPalavra["NE"] = 'null'

            if lista[10][:-1] != '-':

                vetorRel = lista[10][1:-2].split('|')

            dicPalavra["gerarFeature"] = False

            # transforma a string em unicode para o uppercase funcionar nas
            # letras com acento
            lemma = dicPalavra["lemma"].decode('utf-8').upper()
            # Substitui os _ por espaços na string e verifica se ela está
            # no dicionário
            lemma = lemma.encode('utf-8').replace('_', ' ')
            try:
                dic[lemma]
                dicPalavra["dicionario"] = True

            except:
                dicPalavra["dicionario"] = False

            if dicPalavra["ID"] in vetorRel:

                vetorIO.append("I")
                numeroRelacoes += 1

            else:
                vetorIO.append("O")

            vetorEntrada.append(dicPalavra)

            if dicPalavra["NE"] in categoriasUtilizadas:

                if gerarFeatureID is None:

                    gerarFeatureID = int(dicPalavra["ID"])
                    gerarFeatureNE = dicPalavra["NE"]

                else:

                    if dicPalavra["NE"] != gerarFeatureNE:

                        diferenca = int(dicPalavra["ID"]) - gerarFeatureID

                        for index in range(vetorEntrada.index(dicPalavra)-diferenca, vetorEntrada.index(dicPalavra)+1):
                            vetorEntrada[index]["gerarFeature"] = True

    os.mkdir(diretorioTrabalho)
    file = open(diretorioTrabalho+'/vetorDeEntrada.txt', 'a')
    file.write(str(vetorEntrada)+'\n')
    file.close()
    file = open(diretorioTrabalho+'/vetorIO.txt', 'a')
    file.write(str(vetorIO)+'\n')
    file.close()

    for i in range(len(vetorEntrada)):
        if vetorEntrada[i]["gerarFeature"]:
            extrai_features(diretorioTrabalho, vetorEntrada, i)

    return vetorEntrada, numeroRelacoes


def comparar(x, y):

    if x.lower() > y.lower():
        return 1
    elif x.lower() == y.lower():
        return 0
    else:
        return -1


def textosTreinamento(diretorioTrabalho, categUtilizadas, dicionarios, pasta):

    # lista com o nome de todos os arquivos do diretorio
    arquivos = os.listdir(os.path.expanduser(pasta))
    arquivos.sort(comparar)
    entradas = []
    relacoesTotal = 0

    for arquivo in arquivos:
        if(not arquivo.endswith('~')):  # evita arquivos temporários
            textos, relacoesTotalAux = extracaoCogroo(diretorioTrabalho, categUtilizadas, pasta+arquivo, dicionarios)
            relacoesTotal += relacoesTotalAux
            entradas.append((arquivo, textos))

    return entradas, relacoesTotal


# função que gera o vetor de features das palavras marcadas
def extrai_features(diretorioTrabalho, vetor, ind):

    features = dict()

    features["palavra"] = vetor[ind]["lemma"].lower()
    features["palavraOriginal"] = vetor[ind]["lemma"]

    if vetor[ind]["dicionario"]:
        features["dicionario"] = 'sim'
    else:
        features["dicionario"] = 'não'

    if vetor[ind]["Head"] == 'O':
        features["nucleo"] = 'sim'
    else:
        features["nucleo"] = 'nao'

    features["clas"] = vetor[ind]["NE"]
    features["POSTag"] = vetor[ind]["PoS"]
    features["phraseTag"] = vetor[ind]["Structure"]

    tamanho = 2
    iterador = ind
    POSLongRangeSemEN = str()

    # inicio da logica que calcula de onde até onde o programa deve iterar
    while vetor[iterador]["NE"] == 'null':
        iterador -= 1

    if vetor[ind]["NE"] != 'null' and not vetor[ind+1]['gerarFeature']:
        while vetor[iterador-1]["NE"] == 'null':
            iterador -= 1
        iterador -= 1
    # fim da lógica

    while vetor[iterador+1]["NE"] == 'null':  # itera entre as ENs da relacao
        POSLongRangeSemEN = POSLongRangeSemEN + vetor[iterador+1]["PoS"] + " "
        tamanho += 1
        iterador += 1

    features["POSLongRangeSemEN"] = POSLongRangeSemEN[:-1]
    features["tamanho"] = tamanho

    if ind > 0:

        features["prevClas"] = vetor[ind-1]["NE"]
        features["prevW"] = vetor[ind-1]["lemma"].lower()
        features["prevT"] = vetor[ind-1]["PoS"].lower()  # POS
        # NEXT?
        features["next0CT"] = vetor[ind-1]["PoS"] + " " + vetor[ind]["PoS"]  # POS palavras consecutivas
        features["prevPT"] = vetor[ind-1]["Structure"]
        features["prev0CPT"] = vetor[ind-1]["Structure"] + " " + vetor[ind]["Structure"]  # sintatica palavras consecutivas
        # NEXT?
        features["next0CW"] = vetor[ind-1]["lemma"] + " " + vetor[ind]["lemma"]  # palavras consecutivas

    else:

        features["prevClas"] = "null"
        features["prevW"] = "null"
        features["prevT"] = "null"
        features["next0CT"] = "null"
        features["prevPT"] = "null"
        features["prev0CPT"] = "null"
        features["next0CW"] = "null"

    if ind > 1:

        features["prev2Clas"] = vetor[ind-2]["NE"]
        features["prev2W"] = vetor[ind-2]["lemma"].lower()
        features["prev2T"] = vetor[ind-2]["PoS"].lower()  # POS
        features["prev1CT"] = vetor[ind-2]["PoS"] + " " + vetor[ind-1]["PoS"]  # POS palavras consecutivas
        features["prev2PT"] = vetor[ind-2]["Structure"]
        features["prev1CPT"] = vetor[ind-2]["Structure"] + " " + vetor[ind-1]["Structure"]  # sintatica palavras consecutivas
        features["prev1CW"] = vetor[ind-2]["lemma"] + " " + vetor[ind-1]["lemma"]  # palavras consecutivas

    else:

        features["prev2Clas"] = "null"
        features["prev2W"] = "null"
        features["prev2T"] = "null"
        features["prev1CT"] = "null"
        features["prev2PT"] = "null"
        features["prev1CPT"] = "null"
        features["prev1CW"] = "null"

    if ind < len(vetor)-1:

        features["nextClas"] = vetor[ind+1]["NE"]
        features["nextW"] = vetor[ind+1]["lemma"].lower()
        features["nextT"] = vetor[ind+1]["PoS"].lower()  # POS
        features["next1CT"] = vetor[ind]["PoS"] + " " + vetor[ind+1]["PoS"]  # POS palavras consecutivas
        features["nextPT"] = vetor[ind+1]["Structure"]
        features["next1CPT"] = vetor[ind]["Structure"] + " " + vetor[ind+1]["Structure"]  # sintatica palavras consecutivas
        features["next1CW"] = vetor[ind]["lemma"] + " " + vetor[ind+1]["lemma"]  # palavras consecutivas

    else:

        features["nextClas"] = "null"
        features["nextW"] = "null"
        features["nextT"] = "null"
        features["next1CT"] = "null"
        features["nextPT"] = "null"
        features["next1CPT"] = "null"
        features["next1CW"] = "null"

    if ind < len(vetor)-2:

        features["next2Clas"] = vetor[ind+2]["NE"]
        features["next2W"] = vetor[ind+2]["lemma"].lower()
        features["next2T"] = vetor[ind+2]["PoS"].lower()  # POS
        features["next2CT"] = vetor[ind+1]["PoS"] + " " + vetor[ind+2]["PoS"]  # POS palavras consecutivas
        features["next2PT"] = vetor[ind+2]["Structure"]
        features["next2CPT"] = vetor[ind+1]["Structure"] + " " + vetor[ind+2]["Structure"]  # sintatica palavras consecutivas
        features["next2CW"] = vetor[ind+1]["lemma"] + " " + vetor[ind+2]["lemma"]  # palavras consecutivas

    else:

        features["next2Clas"] = "null"
        features["next2W"] = "null"
        features["next2T"] = "null"
        features["next2CT"] = "null"
        features["next2PT"] = "null"
        features["next2CPT"] = "null"
        features["next2CW"] = "null"

    if vetor[ind]["PoS"][0] == "v":
        features["verbo"] = "sim"
    else:
        features["verbo"] = "nao"

    if vetor[ind-1]["PoS"][0] == "v":
        features["prevVerbo"] = "sim"
    else:
        features["prevVerbo"] = "nao"

    if vetor[ind-2]["PoS"][0] == "v":
        features["prev2Verbo"] = "sim"
    else:
        features["prev2Verbo"] = "nao"

    if vetor[ind+1]["PoS"][0] == "v":
        features["nextVerbo"] = "sim"
    else:
        features["nextVerbo"] = "nao"

    if vetor[ind+2]["PoS"][0] == "v":
        features["next2Verbo"] = "sim"
    else:
        features["next2Verbo"] = "nao"

    features["adv"] = "não"
    features["advPrep"] = "não"
    features["advPrepArt"] = "não"
    adverbio = str()

    # verifica se a palavra eh um adverbio
    if(vetor[ind]["PoS"] == "adv"):
            adverbio = "adv"
            if(ind < len(vetor)-1):
                if(vetor[ind+1]["PoS"] == "prp"):  # adverbio seguido de Prep
                    adverbio = "advPrep"
                    if(ind < len(vetor)-2):
                        if(vetor[ind+2]["PoS"] == "art"):  # adverbio seguido de Prep+Art
                            adverbio = "advPrepArt"

    if adverbio == "advPrepArt":
        features["advPrepArt"] = "sim"

    elif adverbio == "advPrep":
        features["advPrep"] = "sim"

    elif adverbio == "adv":
        features["adv"] = "sim"

    print (features)
