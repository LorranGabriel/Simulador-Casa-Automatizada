import socket
import _thread

HOST = '172.16.101.130'             # Endereco IP do Servidor
PORT = 5000                         # Porta que o Servidor esta
lstTM = []
lstLA = []
lstAC = []
lstSP = []
lstTR = []

dicTM = {}
dicLA = {}
dicAC = {}
dicSP = {}
dicTR = {}

def leArq():
    arq = open("resposta_servidor.txt","r")
    txt = arq.read()
    txt = txt.split()
    arq.close()

    return txt

def gerarIDTM(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num) 

def gerarIDLA(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num) 


def gerarIDAC(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num) 

def gerarIDSP(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num)

def gerarIDTR(lst):
    num = len(lst)+1
    lst.append(num)

    return str(num) 

def salvaDic(listaDic):
    print("Chegou")
    arq = open("arq.txt",'w')

    for dic in listaDic:
        chaves = list(dic.keys())
        print(chaves)
        i=0
        while i < len(chaves):
            chave = str(chaves[i])
            conteudo = str(dic[chave])
            arq.write(chave+":"+conteudo+"\n")
            i = i + 1

    arq.close()

def conectado(con, cliente,flag_teste):

    print ('Conectado por', cliente)
    txt = leArq()
    cont = 0
    while True:
        msg = con.recv(1024)
        if not msg: break
        print (cliente, msg.decode())

        if msg.decode() == "TOMADA":
            if flag_teste:
                ambiente = txt[cont]
            else:
                ambiente = input("Informe o ambiente onde se encontra a tomada: ")
            id_dispositivo = gerarIDTM(lstTM)
            con.send(str(id_dispositivo).encode())
            msg = con.recv(1024)
            tm = msg.decode().split(",")

            dicTM[id_dispositivo] = "TOMADA",ambiente
            print(dicTM)

        if msg.decode() == "LAMPADA":
            if flag_teste:
                ambiente = txt[cont]
            else:
                ambiente = input("Informe o ambiente onde se encontra a lampada: ")
            id_dispositivo = gerarIDLA(lstLA)
            con.send(str(id_dispositivo).encode())
            msg = con.recv(1024)
            la = msg.decode().split(",")

            dicLA[id_dispositivo] = "LAMPADA",ambiente
            print(dicLA)

        if msg.decode() == "AR CONDICIONADO":
            if flag_teste:
                ambiente = txt[cont]
            else:
                ambiente = input("Informe o ambiente onde se encontra o ar condicionado: ")
            id_dispositivo = gerarIDAC(lstAC)
            con.send(str(id_dispositivo).encode())
            msg = con.recv(1024)
            ac = msg.decode().split(",")

            dicAC[id_dispositivo] = "AR CONDICIONADO",ambiente

            print(dicAC)           

        if msg.decode() == "SENSOR DE PRESENÇA":
            if flag_teste:
                ambiente = txt[cont]
            else:
                ambiente = input("Informe o ambiente onde se encontra o sensor de presença: ")
            id_dispositivo = gerarIDSP(lstSP)
            con.send((id_dispositivo+","+ambiente).encode())
            msg =	 con.recv(1024)

            sp = msg.decode().split(",")
            presenca = sp[2]
            dicSP[id_dispositivo] = "SENSOR DE PRESENÇA",ambiente,presenca
            print(dicSP)


        if msg.decode() == "TERMOMETRO":
            if flag_teste:
                ambiente = txt[cont]
            else:
                ambiente = input("Informe o ambiente onde se encontra o termometro: ")
            id_dispositivo = gerarIDTR(lstTR)
            con.send(str(id_dispositivo).encode())
            msg = con.recv(1024)

            tr = msg.decode().split(",")
            temperatura = tr[2]
            dicTR[id_dispositivo] = "TERMOMETRO",ambiente,temperatura
            print(dicTR)

            cont += 1

    listaDic = [dicTM,dicLA,dicAC,dicSP,dicTR]
    salvaDic(listaDic)
    print ('Finalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()



tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

flag_teste =  int(input("Deseja fazer teste manual?  1-SIM / 2-NÃO  :"))

while True:
    con, cliente = tcp.accept()
    print("Abrindo novo cliente em nova _thread:")
    _thread.start_new_thread(conectado, tuple([con, cliente,flag_teste]))
    

tcp.close()

