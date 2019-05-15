
#  PROJETO BOLÃO - Fillipe F S Ribeiro

import os

def cadastro_jogador(nome,cpf):
	# FAZ A LEITURA DO NOME na opção 1 do menu
	arq = open('jogadores.txt', 'r')

	cpfs = []
	nomes = []
	lista = arq.read()
	lista_cortada = lista.split()
	for i in lista_cortada:
		if i.isdigit():
			cpfs.append(i)
	arq.close()
	arq = open('jogadores.txt', 'a')

	if cpf in cpfs:
		arq.close()
		flag_confirmação = "CPF ja cadastrado!"
		return flag_confirmação
	else:
		nome = nome + " - "
		cpf = cpf + "\n"
		dados_jogador = nome + cpf
		arq.write(dados_jogador)
		flag_confirmação = "Cadastrado com sucesso"
	arq.close()
	return flag_confirmação

def dicionario_ip():
	# FAZ A LEITURA DO NOME na opção 1 do menu
	arq = open('jogadores.txt', 'r')

	lista = arq.read()
	lista_cortada = lista.split()
	arq.close()
	arq = open('jogadores.txt', 'a')

	
	return lista_cortada


def leitura_jogadores():
	arq = open('jogadores.txt', 'r')
	jogadores = {}
	cpfs = []
	nomes = []
	lista = arq.read()
	lista_cortada = lista.split()
	for i in lista_cortada:
		if i.isdigit():
			cpfs.append(i)
		elif i != "-":
			nomes.append(i)
	arq.close()

	for i in range(len(cpfs)):
		jogadores[nomes[i]] = cpfs[i]

	return jogadores	

def leitura_bilhete():
	arq = open('bilhete.txt', 'r')
	jogadores = leitura_jogadores()
	numeros_list = []
	nomes = []
	apostadores = []
	bilhete_inteiro = []
	lista = arq.read()
	lista_cortada = lista.split()
	cont = 0
	numeros = ""
	apostas =[]
	aux = []
	tupla = ()
	for i in lista_cortada:
		if len(i)==1 and i != "-":
			numeros += i
			cont += 1
		elif i != "-" and len(i) >1:
			if cont > 3:
				apostadores.append(nomes)
				numeros_list.append(numeros)
				numeros = ""
				nomes = []
				cont = 0
			nomes.append(i)
	apostadores.append(nomes)
	numeros_list.append(numeros)		
	arq.close()
	cont = 0

	for j in range(len(apostadores)):
		for k in range(len(apostadores[j])):
			for i in jogadores.items():
				if str(apostadores[j][k]) == i[1]:
					aux.append((i))
		tupla = (aux,numeros_list[j])
		aux = []				
		apostas.append(tupla)
		tupla = ()
		cont+=1


	return apostas	

def lista_Ips(): # exibe os jogadores na opção 2 do menu
	arq = open('jogadores.txt', 'r')
	linha = arq.read()
	arq.close()
	return linha

def removebarraN(text):
	string = ""
	for i in range(len(text)):
		if text[i] != "\n":
			string += text[i]
	return string


def cadastro_aposta(jogadores, bilhete): #OPÇÃO 3 DO MENU
	arq = open('bilhete.txt', 'a')
	flag = True
	str_linha = ""
	listaJogadores = jogadores.split()
	for i in listaJogadores:
		if not i.isdigit():
			flag = False
		if flag:
			str_linha += i + " - "
	for j in bilhete:
		if not j.text.isdigit():
			flag = False
		if flag:
			str_linha += j.text + " "
	if flag == False:
		arq.close()
		return "Não foi possivel cadastrar, tente novamente"
	else:
		str_linha += "\n"
		arq.write(str_linha)
		arq.close()
		return "Cadastrado com sucesso"


def print_aposta(): #EXIBE OS JOGADORES E APOSTAS CADASTRADAS OPÇÃO 4 DO MENU
	arq = open('bilhete.txt', 'r')
	linha = arq.read()
	arq.close()
	return linha

def main():
	return 0

main()
