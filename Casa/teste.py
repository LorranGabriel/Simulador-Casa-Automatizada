import kivy.properties.Property

arq = open('jogadores.txt', 'r')

ips = []
lista = arq.read()
lista_cortada = lista.split("\n")
print(ListProperty(lista_cortada))
arq.close()
arq = open('jogadores.txt', 'a')
