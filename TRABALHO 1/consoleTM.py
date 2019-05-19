import socket
import time
from datetime import datetime
from random import randint

def tomadasCadastradas():
	arq = open("arqTM.txt","r")
	txt = arq.read()
	txt = txt.split()
	arq.close()

	return txt

def leArq():
    arq = open("resposta_cliente_tomada.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

#Console do cliente Tomada = TM
def clienteTM(lista):
	HOST = socket.gethostbyname(socket.gethostname())		# Endereco IP do Servidor
	PORT = 5000												# Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)

	r = 1
	while r == 1:
		tcp.send(("TOMADA").encode())
		id_equipamento,time,msg = (tcp.recv(1024)).decode().split(",")
		print("ID: "+id_equipamento+"     HORA: "+time+"     MSG: "+msg)
		r = int(input("Deseja inserir mais alguma TOMADA?  1-SIM / 2-NÃO  :"))

	#minutos = int(input("Tempo de simulação das tomadas em minutos: "))
	while True :
		tcp.send(("SIMULATOMADA").encode())
		time.sleep(5)    
		numero = randint(0,100)
		tcp.send(str(numero)+","+str(datetime.now()).encode())

	tcp.close()

lista = leArq()
clienteTM(lista)
tomadas = tomadasCadastradas()
print(tomadas)
