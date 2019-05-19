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

    HOST = socket.gethostbyname(socket.gethostname())      	# Endereco IP do Servidor
    PORT = 5000           		                            # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    r = 1
    while r == 1:
        #Indica que o equipamento é do tipo TERMOMETRO e recebe uma id para esse equipamento
        tcp.send(("TERMOMETRO").encode())
        id_equipamento,time,msg = (tcp.recv(1024)).decode().split(",")
        temperatura = input("Indique a temperatura em graus Celsius do termometro " + id_equipamento +": ")
        tcp.send((id_equipamento+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+temperatura).encode())
        print("ID: "+id_equipamento+"     HORA: "+time+"     MSG: "+msg)
        r = int(input("Deseja inserir mais algum TERMOMETRO?  1-SIM / 2-NÃO  :"))


    tcp.close()

lista = leArq()
clienteTR(lista)