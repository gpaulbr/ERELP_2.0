# coding=utf-8
import extracaoCogroo
import time
import os

displaytime = time.strftime("%x %X", time.localtime())
diretorioTrabalho = './saida_ORG_PES_Gabriel'+'_'+str(displaytime.replace('/', '-'))
categorias = ['PES', 'ORG']
dicionarios = ['../Dicionarios/Profissao_Titulo.txt']  # , '../Dicionarios/Localizacao.txt']
os.mkdir(diretorioTrabalho)
entrada, relacoes = extracaoCogroo.textosTreinamento(diretorioTrabalho, categorias, dicionarios, './entrada/')

# file = open('./saida/saida.txt', 'a')
# file.write(str(entrada))
# file.close()

print ('--------------------------------------------------')
print entrada
print ('--------------------------------------------------')
print relacoes
