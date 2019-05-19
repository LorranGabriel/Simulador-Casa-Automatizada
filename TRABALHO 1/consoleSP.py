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
    HOST = socket.gethostbyname(socket.gethostname())           # Endereco IP do Servidor
    PORT = 5000                                                 # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)

    r = 1
    while r == 1:
        tcp.send(("SENSOR DE PRESENÇA").encode())
        id_equipamento,ambiente = (tcp.recv(1024)).decode().split(",")
        presenca = input("Existem pessoas no(a)"+ambiente +": 1-SIM / 2-NÃO ")
        tcp.send((id_equipamento+","+str(datetime.now())+","+presenca).encode())
        id_equipamento,time,msg = (tcp.recv(1024)).decode().split(",")
        print("ID: "+id_equipamento+"     HORA: "+time+"     MSG: "+msg)
        r = int(input("Deseja inserir mais algum SENSOR DE PRESENÇA?  1-SIM / 2-NÃO  : "))
    tcp.send(("SIMULASP").encode())
    tcp.close()

lista = leArq()
clienteSP(lista)
