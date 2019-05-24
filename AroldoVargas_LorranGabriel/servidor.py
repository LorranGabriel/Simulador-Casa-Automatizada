import socket
import _thread
from datetime import datetime

HOST = socket.gethostbyname(socket.gethostname())		# Endereco IP do Servidor
PORT = 5000												# Porta que o Servidor esta

lstTM = []
lstLA = []
lstAC = []
lstSP = []
lstTR = []

dicTM = {}
dicLA = {}
dicAC = {}
dicSP = {}
dicTR = {}
dicTR_alterado = {}


def leArq():
    arq = open("resposta_servidor.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

def alteraPresenca(dic,msg,flag):
	print("cheguei")
	lst = msg.split(",")

	for chave in dic:
		if chave in lst:
			dic[chave][2] = flag

	return dic


def verificaTemperatura(dic_ar,dic_termometro):

	registro = open("Registro.txt","a")

	lista_temp = []
	new_dic_temp = {}
	temperatura = ""
	comodo = ""
	if dic_termometro != {} and dic_ar != {}:
		for i in dic_termometro.keys():
			valor_termometro = dic_termometro[i]
			temperatura = valor_termometro[2]
			comodo = valor_termometro[1]
			for j in dic_ar.keys():
				valor_ar = dic_ar[j]
				if valor_termometro[1].lower() == valor_ar[1].lower():
					if int(valor_termometro[2]) > 27:
						temperatura = '22'
						comodo = valor_termometro[1]
						registro.write("Temperatura de termometro "+str(i)+" atualizada de acordo com AR" + "\n")
			new_dic_temp[i]=('TERMOMETRO',comodo,temperatura)
	else:
		registro.close()
		return	dic_termometro
	
	registro.close()
	return (new_dic_temp)




def verificaPresenca(dic):
	lst = []
	for chave in dic:
		#Significa que existem pessoas no ambiente
		if dic[chave][2] == "1":
			lst.append(dic[chave][1])

	return lst

#Dicionario das lampadas e lista com ambientes que possuem presenca
def ligarLampada(dic,lst):
	for chave in dic:
		#Significa que a lampada esta em um ambiente com presenca logo deve ser ligada
		if dic[chave][1] in lst:
			dic[chave][2] = "ligada"

	return dic

def gerarIDTM(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num) 

def gerarIDLA(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num) 


def gerarIDAC(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num) 

def gerarIDSP(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num)

def gerarIDTR(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num)

def salvaConsumo(valor,hora):
	valor = str(valor)
	hora = str(hora)
	arq = open("consumo.txt",'a')
	arq.write("HORA: "+hora+"   CONSUMO:"+valor+"\n")

	arq.close()

def salvaDic(dic,a):
    arq = open(a,'w')

    chaves = list(dic.keys())
    i=0
    while i < len(chaves):
        chave = str(chaves[i])
        conteudo = str(dic[chave])
        arq.write(chave+":"+conteudo+"\n")
        i = i + 1

    arq.close()

def conectado(con, cliente):
	print ('Conectado por', cliente)

	while True:
		registro = open("Registro.txt","a")

		msg = con.recv(1024)
		if not msg: break
		tipo_dispositivo = msg.decode()

		if msg.decode() == "TOMADA":
			id_dispositivo = gerarIDTM(lstTM)
			ambiente = input("Insira o ambiente onde a TOMADA "+id_dispositivo+" foi inserida: ")
			con.send((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("TOMADA "+id_dispositivo+" inserida com sucesso!")).encode())
			registro.write((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("TOMADA "+id_dispositivo+" inserida em " + ambiente + "\n")))
			dicTM[id_dispositivo] = ["TOMADA",ambiente]

		if msg.decode() == "SIMULAÇÃO DO CONSUMO DAS TOMADAS":
			msg = con.recv(1024)
			tm = msg.decode().split(",")
			consumo = tm[0]
			time = tm[1]
			salvaConsumo(consumo,time)

		if msg.decode() == "LAMPADA":
			id_dispositivo = gerarIDLA(lstLA)
			ambiente = input("Ambiente onde a LAMPADA "+id_dispositivo+" foi inserida: ")
			con.send((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("LAMPADA "+id_dispositivo+" inserida com sucesso!")).encode())
			registro.write((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("LAMPADA "+id_dispositivo+" inserida em " + ambiente+ "\n")))

			dicLA[id_dispositivo] = ["LAMPADA",ambiente,"desligada"]

		if msg.decode() == "AR CONDICIONADO":       
			id_dispositivo = gerarIDAC(lstAC)
			ambiente = input("Ambiente onde o AR CONDICIONADO "+id_dispositivo+" foi inserido: ")
			con.send((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("AR CONDICIONADO "+id_dispositivo+" inserido com sucesso!")).encode())
			registro.write((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("AR CONDICIONADO "+id_dispositivo+" inserido em " + ambiente+ "\n")))

			msg = con.recv(1024)
			ac = msg.decode().split(",")
			print(ac)
			id = ac[0]
			time = ac[1]
			estado = ac[2]

			print("ID: "+id+"     HORA: "+time+"     MSG: "+estado)

			if int(datetime.now().strftime("%H")) >= 18:
				dicAC[id_dispositivo] = ["AR CONDICIONADO",ambiente,"ligado"]
				registro.write("Estado de AR CONDICIONADO "+str(id_dispositivo)+" atualizado para ligado de acordo com horario programado" + "\n")
      
			else:
				dicAC[id_dispositivo] = ["AR CONDICIONADO",ambiente,estado]

		if msg.decode() == "SENSOR DE PRESENÇA":
			#Gera um ID sequencial para o dispositivo
			id_dispositivo = gerarIDSP(lstSP)
			#Solicita ao usuário o ambiente onde o dispositivo foi instalado
			ambiente = input("Ambiente onde o SENSOR DE PRESENÇA "+id_dispositivo+" foi inserido: ")
			#Envia mensagem para o dispositivo informando seu ID e o ambiente aonde esta localizado
			con.send((id_dispositivo+","+ambiente).encode())
			msg = con.recv(1024)
			sp = msg.decode().split(",")
			id = sp[0]
			time = sp[1]
			presenca = sp[2]
			print("ID: "+id+"     HORA: "+time+"     MSG: "+presenca)
			con.send((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("SENSOR DE PRESENÇA "+id_dispositivo+" inserido com sucesso!")).encode())
			registro.write((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("SENSOR DE PRESENÇA "+id_dispositivo+" inserido em " + ambiente+ "\n")))

			dicSP[id_dispositivo] = ["SENSOR DE PRESENÇA",ambiente,presenca]
         

		if msg.decode() == "TERMOMETRO":
			#Gera um ID sequencial para o dispositivo
			id_dispositivo = gerarIDTR(lstTR)
			#Solicita ao usuário o ambiente onde o dispositivo foi instalado
			ambiente = input("Ambiente onde o TERMOMETRO "+id_dispositivo+" foi inserido: ")
			#Envia mensagem para o dispositivo informando seu ID
			con.send((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("TERMOMETRO "+id_dispositivo+" inserido com sucesso!")).encode())
			registro.write((id_dispositivo+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+("TERMOMETRO "+id_dispositivo+" inserido em " + ambiente+ "\n")))

			msg = con.recv(1024)
			tr = msg.decode().split(",")
			id = tr[0]
			time = tr[1]
			temperatura = tr[2]
			print("ID: "+id+"     HORA: "+time+"     MSG: "+temperatura)
			dicTR[id_dispositivo] = ["TERMOMETRO",ambiente,temperatura]
          
		#print (cliente, tipo_dispositivo)
		registro.close()

		#Salva os dicionarios com as informações dos dispositivos em seus respectivos arquivos de texto
		if dicTR:
			dicTR_alterado = verificaTemperatura(dicAC,dicTR)
			salvaDic(dicTR_alterado,"arqTR.txt")
		if dicTM:
			salvaDic(dicTM,"arqTM.txt")
		if dicSP:
			salvaDic(dicSP,"arqSP.txt")
			if msg.decode() ==  "simularSP":
				msg = con.recv(1024)
				sp = msg.decode().split(",")
				hora = sp[0]
				msgLigar = sp[1]
				print(msgLigar)
				dic = alteraPresenca(dicSP,msgLigar,1)
				salvaDic(dic,"arqSP.txt")

				msg = con.recv(1024)
				sp = msg.decode().split(",")
				hora = sp[0]
				msgDesligar = sp[1]
				print(msgDesligar)
				dic = alteraPresenca(dicSP,msgDesligar,2)		
				salvaDic(dic,"arqSP.txt")
		if dicAC:
			salvaDic(dicAC,"arqAC.txt")
		if dicLA:
			salvaDic(dicLA,"arqLA.txt")
			lstAmbientes = verificaPresenca(dicSP)
			if msg.decode() ==  "simularLA":
				dic = ligarLampada(dicLA,lstAmbientes)			
				novamsg =""
				for chave in dic:
					id_dispositivo = chave
					estado = dic[chave][2]
					mensag = id_dispositivo+":"+estado
					novamsg = novamsg+"-"+mensag

				con.send((novamsg).encode())

				salvaDic(dic,"arqLA.txt")

	print ('Finalizando conexao do cliente', cliente)
	#con.close()
	_thread.exit()


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    _thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
