import socket
from datetime import datetime
import time

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
    lst = []
    r = 1
    while r == 1:
        tcp.send(("SENSOR DE PRESENÇA").encode())
        id_equipamento,ambiente = (tcp.recv(1024)).decode().split(",")
        presenca = input("Existem pessoas no(a)"+ambiente +": 1-SIM / 2-NÃO ")
        lst.append([id_equipamento,ambiente,presenca])
        tcp.send((id_equipamento+","+(datetime.now().strftime("%d/%m/%Y %H:%M"))+","+presenca).encode())
        id_equipamento,hora,msg = (tcp.recv(1024)).decode().split(",")
        print("ID: "+id_equipamento+"     HORA: "+hora+"     MSG: "+msg)
        r = int(input("Deseja inserir mais algum SENSOR DE PRESENÇA?  1-SIM / 2-NÃO  : "))
    

    tcp.send(("simularSP").encode())
    while True:
        msgLigar = ""
        msgDesligar = ""
        time.sleep(5) 
        for equipamento in lst:
            res = input("Existem pessoas no(a)"+equipamento[1] +": 1-SIM / 2-NÃO ")
            if res == "1":
                msgLigar = msgLigar+","+equipamento[0]
            else:
                msgDesligar = msgDesligar+","+equipamento[0]
                 
        tcp.send(((datetime.now().strftime("%d/%m/%Y %H:%M"))+","+msgLigar).encode())
        time.sleep(10)
        tcp.send(((datetime.now().strftime("%d/%m/%Y %H:%M"))+","+msgDesligar).encode())


    tcp.close()

lista = leArq()
clienteSP(lista)
