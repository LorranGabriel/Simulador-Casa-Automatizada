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
	HOST = socket.gethostbyname(socket.gethostname())      	# Endereco IP do Servidor
	PORT = 5000           									# Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	tcp.connect(dest)

	r = 1
	while r == 1:
		tcp.send(("AR CONDICIONADO").encode())
		id_equipamento,time,msg = (tcp.recv(1024)).decode()
		temp = input("Qual é a temperatura padrão do AR CONDICIONADO "+id_equipamento+" em graus Celsius: ")
		tcp.send((id_equipamento+","+str(datetime.now())+","+temp).encode())
		print("ID: "+id_equipamento+"     HORA: "+time+"     MSG: "+msg)
		r = int(input("Deseja inserir mais algum AR CONDICIONADO?  1-SIM / 2-NÃO  :"))

	tcp.close()

lista = leArq()
clienteAC(lista)