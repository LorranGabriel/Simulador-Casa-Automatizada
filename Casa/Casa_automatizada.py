
# -*- coding: utf-8 -*-

import sys

if sys.platform == 'linux2':
    import subprocess
    output = subprocess.Popen(
        'xrandr | grep "\*" | cut -d" " -f4',
        shell=True,
        stdout=subprocess.PIPE).communicate()[0]
    screenx = int(output.replace('\n', '').split('x')[0])
    screeny = int(output.replace('\n', '').split('x')[1])
elif sys.platform == 'win32':
    from win32api import GetSystemMetrics
    screenx = GetSystemMetrics(0)
    screeny = GetSystemMetrics(1)
elif sys.platform == 'darwin':
    from AppKit import NSScreen
    frame_size = NSScreen.mainScreen().frame().size
    screenx = frame_size.width
    screeny = frame_size.height
else:
    # For mobile devices, use full screen
    screenx,screeny = 800,600  # return something

import kivy
from kivy.app import App
from kivy.app import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import casa_api
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
import time
kivy.require('1.8.0')
 
__version__ = "0.1"



Window.size = (1324,800)
Window.left = (screenx - 1200)/2
Window.top = (screeny - 800)/2
hora = ""
temperatura = ""
data = ""

numeros_sorteados = []
jogadores = {}
bilhete = []
div = 0.0
 
class HomeWidget(Screen):



    pass
 
class DispositivosWidget(Screen):
	pass

class Celular(Screen):
	pass

class Bolao_Janela(ScreenManager):



	# spinner = Spinner(
 #    # default value shown
 #    text='Home',
 #    # available values
 #    values=('Home', 'Work', 'Other', 'Custom'),
 #    # just for positioning in our example
 #    size_hint=(None, None),
 #    size=(100, 44),
 #    pos_hint={'center_x': .5, 'center_y': .5})

	def show_selected_value(self):
		runTouchApp(mainbutton)

	def on_remove_botao(self):
		self.remove_wigdet(self.dropdown)

	def switch_to_homeWidget(self):
	    self.current = 'homeWidget'	
	
	def switch_to_dispositivosWidget(self):
		self.current = 'dispositivosWidget'



	def init_simulacao(self,clocktext):
		Clock.schedule_interval(self.update(clocktext), 1) 

	def update(self,clocktext):
		clocktext.text = time.strftime('%I'+':'+'%M'+' %p')

	def simulacao(self,cont):
		horaLabel = StringProperty()
		dataLabel = StringProperty()
		temperaturaLabel = StringProperty()
		celularImagem = StringProperty()
		celularLabel = StringProperty()
		telaImagem = StringProperty()
		telaLabel = StringProperty()
		boxCelular = StringProperty()
		quarto1Lista = StringProperty()
		quarto2Lista = StringProperty()
		cozinhaLista = StringProperty()
		salaLista = StringProperty()
		corredorLista = StringProperty()
		banheiroLista = StringProperty()	 
		lista = [horaLabel,dataLabel,temperaturaLabel]

		arq = open("Inicio.txt","r")
		linha = arq.readline()
		cont = 0
		while linha != "":
			linha = casa_api.removebarraN(linha)
			if cont == 2:
				lista[cont].txt = linha
			linha = arq.readline()
			cont +=1
		arq.close()

		celularImagem.source = "celular.png"
		celularLabel.background_color = 1,1,1,1
		telaImagem.source = "tela.png"
		telaLabel.background_color = 0,0,0,0
		boxCelular.background_color = 0,0,0,1
		boxCelular.text = "Enviar"

		telaLabel.text = "Relatorio de sistema"
		
		listaAr = []
		listaAr.append(quarto1Lista[2])
		listaAr.append(quarto2Lista[2])
		listaAr.append(cozinhaLista[2])
		listaAr.append(salaLista[2])
		listaAr.append(corredorLista[2])
		listaAr.append(banheiroLista[2])


		listaTemp = []
		listaTemp.append(quarto1Lista[0])
		listaTemp.append(quarto2Lista[0])
		listaTemp.append(cozinhaLista[0])
		listaTemp.append(salaLista[0])
		listaTemp.append(corredorLista[0])
		listaTemp.append(banheiroLista[0])


		listaPresenca = []
		listaPresenca.append(quarto1Lista[1])
		listaPresenca.append(quarto2Lista[1])
		listaPresenca.append(cozinhaLista[1])
		listaPresenca.append(salaLista[1])
		listaPresenca.append(corredorLista[1])
		listaPresenca.append(banheiroLista[1])

		listaLampadas = []
		listaLampadas.append(quarto1Lista[3])
		listaLampadas.append(quarto2Lista[3])
		listaLampadas.append(cozinhaLista[3])
		listaLampadas.append(salaLista[3])
		listaLampadas.append(corredorLista[3])
		listaLampadas.append(banheiroLista[3])	

		Arligado = [["arQuarto1",0],["arQuarto2",0],["arCozinha",0],["arSala",0],["arCorredor",0],["arBanheiro",0]]

		#Não tem ar na cozinha e no banheiro
		Sensortemp = [["tempQuarto1",1,"25"],["tempQuarto2",1,"25"],["tempCozinha",1,"25"],["tempSala",1,"25"],["tempCorredor",1,"25"],["tempBanheiro",1,"25"]]
		Presenca = [["pessoasQuarto1",1],["pessoasQuarto2",0],["pessoasCozinha",0],["pessoasSala",1],["pessoasCorredor",0],["pessoasBanheiro",0]]

		Lampadas = [["lampadaQuarto1",1,1],["lampadaQuarto2",1,1],["lampadaCozinha",1,0],["lampadaSala",1,1],["lampadaCorredor1",1,0],["lampadaBanheiro",1,0]]

			#Preenche imagem Ar

		for j in Arligado:
			if j[1] == 1 and (j[0] == "arQuarto1" or j[0] == "arQuarto2"):
				if j[0] == "arQuarto1":
					listaAr[0].source = "arcondicionadoDir.png"
				if j[0] == "arQuarto2":
					listaAr[1].source = "arcondicionadoDir.png"

			if j[1] == 1 and j[0] == "arCorredor":
				listaAr[4].source = "arcondicionadoFrente.png"
			
			if j[1] == 1 and j[0] == "arSala":
				listaAr[3].source = "arcondicionadoEsq.png"


		#Preenche Temperatura

		for j in Sensortemp:
			if j[1] == 1 and (j[0] == "tempQuarto1" or j[0] == "tempQuarto2"):
				if j[0] == "tempQuarto1":
					listaTemp[0].text = j[2] + "°"
				if j[0] == "tempQuarto2":
					listaTemp[1].text = j[2] + "°"

			if j[1] == 1 and j[0] == "tempSala":
				listaTemp[3].text = j[2] + "°"
			
			if j[1] == 1 and j[0] == "tempCozinha":
				listaTemp[2].text = j[2] + "°"

			if j[1] == 1 and j[0] == "tempCorredor":
				listaTemp[4].text = j[2] + "°"

			if j[1] == 1 and j[0] == "tempBanheiro":
				listaTemp[5].text = j[2] + "°"


		#Preenche Prensença

		for j in Presenca:
			if j[1] == 1 and (j[0] == "pessoasQuarto1" or j[0] == "pessoasQuarto2"):
				if j[0] == "pessoasQuarto1":
					listaPresenca[0].text = "s"
				if j[0] == "pessoasQuarto2":
					listaPresenca[1].text = "s"

			if j[1] == 1 and j[0] == "pessoasSala":
				listaPresenca[3].text = "s"
			
			if j[1] == 1 and j[0] == "pessoasCozinha":
				listaPresenca[2].text = "s"

			if j[1] == 1 and j[0] == "pessoasCorredor":
				listaPresenca[4].text = "s"

			if j[1] == 1 and j[0] == "pessoasBanheiro":
				listaPresenca[5].text ="s"



		for j in Lampadas:
			if j[2]==1:
				if j[1] == 1 and (j[0] == "lampadaQuarto1" or j[0] == "lampadaQuarto2"):
					if j[0] == "lampadaQuarto1":
						listaLampadas[0].source = "lampada_acesa.png"
					if j[0] == "lampadaQuarto2":
						listaLampadas[1].source = "lampada_acesa.png"

				if j[1] == 1 and j[0] == "lampadaSala":
					listaLampadas[3].source = "lampada_acesa.png"
				
				if j[1] == 1 and j[0] == "lampadaCozinha":
					listaLampadas[2].source = "lampada_acesa.png"

				if j[1] == 1 and j[0] == "lampadaCorredor1":
					listaLampadas[4][0].source = "lampada_acesa.png"
					listaLampadas[4][1].source = "lampada_acesa.png"
				if j[1] == 1 and j[0] == "lampadaBanheiro":
					listaLampadas[5].source ="lampada_acesa.png"
			else:
				if j[1] == 1 and (j[0] == "lampadaQuarto1" or j[0] == "lampadaQuarto2"):
					if j[0] == "lampadaQuarto1":
						listaLampadas[0].source = "lampada_apagada.png"
					if j[0] == "lampadaQuarto2":
						listaLampadas[1].source = "lampada_apagada.png"

				if j[1] == 1 and j[0] == "lampadaSala":
					listaLampadas[3].source = "lampada_apagada.png"
				
				if j[1] == 1 and j[0] == "lampadaCozinha":
					listaLampadas[2].source = "lampada_apagada.png"

				if j[1] == 1 and j[0] == "lampadaCorredor1":
					listaLampadas[4][0].source = "lampada_apagada.png"
					listaLampadas[4][1].source = "lampada_apagada.png"

				if j[1] == 1 and j[0] == "lampadaBanheiro":
					listaLampadas[5].source ="lampada_apagada.png"





			if horaLabel.text == '':
				horaLabel.text = str(1)
			else:
				horaLabel.text = str(int(horaLabel.text)+1)
			break
		

		return 0



	def callbackHome(self):
		dataLabel = StringProperty()
		arq = open("Inicio.txt","w")
		arq.write(str(horaLabel1)+"\n"+str(temperaturaLabel)+"\n"+str(dataLabel)+"\n")
		arq.close()




	# def show_selected_value(spinner, text):
	# 	print('The spinner', spinner, 'have text', text)
	# 	runTouchApp(spinner)
	# spinner.bind(text=show_selected_value)

class casa(App):

	
	def __init__(self,**kwargs):
		super(casa,self).__init__(**kwargs)
		#Lista [temperatura,numeroPessoas,arCoondicionado,lampadas,tomadas]
		
	
	def build(self):
		self.root = Bolao_Janela()


		return self.root

	# 
	# 
if __name__ == '__main__':
    casa().run()
