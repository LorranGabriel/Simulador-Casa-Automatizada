import socket
from datetime import datetime

def leArq():
    arq = open("resposta_cliente_ar.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

#Console do cliente Ar Condicionado = AC
def clienteAC():
	HOST = socket.gethostbyname(socket.gethostname())      	# Endereco IP do Servidor
	PORT = 5000           									# Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)

	r = 1
	while r == 1:
		tcp.send(("AR CONDICIONADO").encode())
		id_equipamento,time,msg = (tcp.recv(1024)).decode().split(",")
		temp = int(input("Qual se o AR CONDICIONADO "+id_equipamento+" esta ligado: 1-SIM / 2-NÃO "))
		if temp == 1:
			tcp.send((id_equipamento+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+"ligado").encode())
		else:
			tcp.send((id_equipamento+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+"desligado").encode())

		print("ID: "+id_equipamento+"     HORA: "+time+"     MSG: "+msg)
		r = int(input("Deseja inserir mais algum AR CONDICIONADO?  1-SIM / 2-NÃO  :"))

	tcp.close()

clienteAC()