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


def leArq():
    arq = open("resposta_servidor.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt


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
		msg = con.recv(1024)
		if not msg: break
		tipo_dispositivo = msg.decode()

		if msg.decode() == "TOMADA":
			id_dispositivo = gerarIDTM(lstTM)
			ambiente = input("Insira o ambiente onde a TOMADA "+id_dispositivo+" foi inserida: ")
			con.send((id_dispositivo+","+str(datetime.now())+","+("TOMADA "+id_dispositivo+" inserida com sucesso!")).encode())

			dicTM[id_dispositivo] = ["TOMADA",ambiente]

		if msg.decode() == "SIMULATOMADA":
			msg = con.recv(1024)
			tm = msg.decode().split(",")
			consumo = [0]
			time = [1]
			salvaConsumo(consumo,str(time))

		if msg.decode() == "LAMPADA":
			id_dispositivo = gerarIDLA(lstLA)
			ambiente = input("Ambiente onde a LAMPADA "+id_dispositivo+" foi inserida: ")
			con.send((id_dispositivo+","+str(datetime.now())+","+("LAMPADA "+id_dispositivo+" inserida com sucesso!")).encode())

			dicLA[id_dispositivo] = ["LAMPADA",ambiente,"desligada"]

		if msg.decode() == "AR CONDICIONADO":       
			id_dispositivo = gerarIDAC(lstAC)
			ambiente = input("Ambiente onde o AR CONDICIONADO "+id_dispositivo+" foi inserido: ")
			con.send((id_dispositivo+","+str(datetime.now())+","+("AR CONDICIONADO "+id_dispositivo+" inserido com sucesso!")).encode())

			msg = con.recv(1024)
			ac = msg.decode().split(",")
			id = ac[0]
			time = ac[1]
			temPadrao = ac[2]

			print("ID: "+id+"     HORA: "+time+"     MSG: "+temPadrao)

			dicAC[id_dispositivo] = ["AR CONDICIONADO",ambiente,temPadrao]      

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
			con.send((id_dispositivo+","+str(datetime.now())+","+("SENSOR DE PRESENÇA "+id_dispositivo+" inserido com sucesso!")).encode())

			dicSP[id_dispositivo] = ["SENSOR DE PRESENÇA",ambiente,presenca]
         

		if msg.decode() == "TERMOMETRO":
			#Gera um ID sequencial para o dispositivo
			id_dispositivo = gerarIDTR(lstTR)
			#Solicita ao usuário o ambiente onde o dispositivo foi instalado
			ambiente = input("Ambiente onde o TERMOMETRO "+id_dispositivo+" foi inserido: ")
			#Envia mensagem para o dispositivo informando seu ID
			con.send((id_dispositivo+","+str(datetime.now())+","+("TERMOMETRO "+id_dispositivo+" inserido com sucesso!")).encode())

			msg = con.recv(1024)
			tr = msg.decode().split(",")
			id = tr[0]
			time = tr[1]
			temperatura = tr[2]
			print("ID: "+id+"     HORA: "+time+"     MSG: "+temperatura)
			dicTR[id_dispositivo] = ["TERMOMETRO",ambiente,temperatura]

          
		print (cliente, tipo_dispositivo)

		#Salva os dicionarios com as informações dos dispositivos em seus respectivos arquivos de texto
		if dicTR:
			salvaDic(dicTR,"arqTR.txt")
		if dicTM:
			salvaDic(dicTM,"arqTM.txt")
		if dicSP:
			salvaDic(dicSP,"arqSP.txt")
		if dicAC:
			salvaDic(dicAC,"arqAC.txt")
		if dicLA:
			salvaDic(dicLA,"arqLA.txt")
			''' TEM QUE FAZER AQUI, PROCESSO PARA LIGAR AS LAMPADAS
			lstAmbientes = verificaPresenca(dicSP)
			if msg.decode() ==  "simularLA":
				print("cheguei")
				dic = ligarLampada(dicLA,lstAmbientes)
				print(dic)
				for chave in dic:
					id_dispositivo = dic[chave][0]
					estado = dic[chave][2]
					con.send((id_dispositivo+","+str(datetime.now())+","+("LAMPADA "+id_dispositivo)).encode())

				salvaDic(dicLA,"arqLA.txt")'''

	

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

