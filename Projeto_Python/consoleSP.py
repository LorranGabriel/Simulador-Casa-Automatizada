import socket
from datetime import datetime

def leArq():
    arq = open("resposta_cliente_sensor.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

#Função do cliente Sensor de Presença = SP
def clienteSP(lista):
    HOST = '172.17.106.73'     	# Endereco IP do Servidor
    PORT = 5000           		# Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    cont = 0
    r = 1
    while r == 1:
        tcp.send(("SENSOR DE PRESENÇA").encode())
        id_equipamento,ambiente = (tcp.recv(1024)).decode().split(",")
		#presenca = input("Existem pessoas no(a)"+ambiente +": 1-SIM / 2-NÃO ")
        presenca = lista[cont]
        tcp.send((id_equipamento+","+str(datetime.now())+","+presenca).encode())
        cont += 1
        #r =  int(input("Deseja inserir mais algum SENSOR DE PRESENÇA?  1-SIM / 2-NÃO  :"))
        r =  int(lista[cont])
        cont += 1
    tcp.send(("terminou").encode())
    tcp.close()

lista = leArq()
clienteSP(lista)
