############################################################
# Estudo do Kivy
# www.cadernodelaboratorio.com.br
# Acompanha a nota "Compreendendo os eventos em Kivy
# por Roberto Tavares, em 23/07/2015
############################################################
 
import kivy
kivy.require('1.7.0')
 
__version__ = "0.1.1"
 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty,NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label

import time

class CronoWidget(BoxLayout):
    cronoValue = NumericProperty()
    cronoValueText1 = StringProperty()
 
    def update(self, *args):
        self.cronoValueText1= str(self.cronoValue)
        self.cronoValue += 1
 


class exp14b(App):

    def build(self):
        cronos = CronoWidget()
        cronos.cronoValue=0
        Clock.schedule_interval(cronos.update,1)
        return cronos      
 
if __name__ == '__main__':
    exp14b().run()   