import socket
from datetime import datetime
 
def leArq():
    arq = open("resposta_cliente_lampada.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

#Console do cliente Lampada = LA
def clienteLA(lista):
	HOST = '172.17.106.73'     	# Endereco IP do Servidor
	PORT = 5000           		# Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)
	
	r = 1
	while r == 1:
		tcp.send(("LAMPADA").encode())
		id_equipamento = (tcp.recv(1024)).decode()
		r =  int(input("Deseja inserir mais alguma LAMPADA?  1-SIM / 2-NÃO  :"))

	tcp.close()


lista = leArq()
clienteLA(lista)
