import socket
from datetime import datetime
 
def leArq():
    arq = open("resposta_cliente_termometro.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

#Função do cliente Termmometro = TR
def clienteTR(lista):

    HOST = '172.17.106.73'     	# Endereco IP do Servidor
    PORT = 5000           		# Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    cont = 0

    r = 1
    while r == 1:
        #Indica que o equipamento é do tipo TERMOMETRO e recebe uma id para esse equipamento
        tcp.send(("TERMOMETRO").encode())
        id_equipamento = (tcp.recv(1024)).decode()

    	#temperatura = input("Indique a temperatura em graus Celsius do termometro " + id_equipamento +": ")
        temperatura = lista[cont]
        cont+=1
        tcp.send((id_equipamento+","+str(datetime.now())+","+temperatura).encode())
        #r =  int(input("Deseja inserir mais algum TERMOMETRO?  1-SIM / 2-NÃO  :"))
        r = int(lista[cont])
        cont+=1

    tcp.send(("terminou").encode())
    tcp.close()

lista = leArq()
clienteTR(lista)