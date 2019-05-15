import socket
from datetime import datetime

def leArq():
    arq = open("resposta_cliente_ar.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

#Console do cliente Ar Condicionado = AC
def clienteAC(lista):
	HOST = '172.17.106.73'     	# Endereco IP do Servidor
	PORT = 5000           		# Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)
	
	r = 1
	while r == 1:
		tcp.send(("AR CONDICIONADO").encode())
		id_equipamento = (tcp.recv(1024)).decode()
		r =  int(input("Deseja inserir mais algum AR CONDICIONADO?  1-SIM / 2-NÃO  :"))

	tcp.close()

lista = leArq()
clienteAC(lista)