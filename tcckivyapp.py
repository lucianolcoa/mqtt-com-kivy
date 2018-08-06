from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, FadeTransition
from  kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty,StringProperty,BooleanProperty,ListProperty,ObjectProperty
from kivy.graphics.vertex_instructions import (Rectangle,Ellipse,Line)
from kivy.graphics.context_instructions import Color
import time
from datetime import datetime, timedelta
import serial
import sqlite3
import time
import datetime
import os

import paho.mqtt.client as mqtt


class telaprincipal(ScreenManager):
    pass
class Telasensor(Screen):

   mqtt=BooleanProperty()
   temperatura=NumericProperty()
   umidade=NumericProperty()
   grafico=NumericProperty()
   strumidade=StringProperty()
   agua=NumericProperty()
   strtimer=StringProperty()
   timer=NumericProperty()
   tamanho=NumericProperty()
   xantt=NumericProperty()
   xatualt=NumericProperty()
   yantt=NumericProperty()
   yatualt=NumericProperty()
   listat=ListProperty()
   xantu=NumericProperty()
   xatualu=NumericProperty()
   yantu=NumericProperty()
   yatualu=NumericProperty()
   listau=ListProperty()
   listaa=ListProperty()
   vira=BooleanProperty()
   stragua=StringProperty()
   strtemperatura=StringProperty()
   luz=NumericProperty()
   strluz=StringProperty()
   aviso=StringProperty()
   aviso1=StringProperty()
   sba=StringProperty()
   ba=NumericProperty()
   conta=NumericProperty()
   conta2=NumericProperty()
   
   def __init__(self,**kwargs):
       self.mqtt=False
       self.tamanho=1
       self.vira=True
       super(Telasensor,self).__init__(**kwargs)
       
       Clock.schedule_interval(self.update,2)
       self.xantt=0
       self.xatualt=1
       self.yantt=self.height
       self.yatualt=self.height+1
       self.xantu=0
       self.xatualu=1
       self.yantu=2*self.height
       self.yatualt=2*self.height+1
       self.xatualu=0
       self.xantu=0
       self.xanta=0
       self.xatuala=1
       self.yanta=0
       self.yatuala=2*self.height+1
       self.temperatura=20
       self.agua=80
       self.conta=0
       self.conta2=0
       
   def ligamqtt(self):
       if self.mqtt==False:
           self.aviso="ligado"
           self.mqtt=True
       else:
           self.mqtt=False
   def on_connect(self,client, userdata, flags, rc):
    
    client.subscribe("EMCOL/#")

   def on_message(self,client, userdata, msg):
    print (msg.payload) 
    print ('funcionando')   
    self.update()   
   def update(self,*args):
       
       
       #configurando o broker mqtt
       
       #pegando as variaveis por mqtt
       
       
             
       if self.mqtt==True:
          
           self.client = mqtt.Client()
           

           self.client.username_pw_set("ouccoeks", password="F-vr8zrNgD7q")

           self.client.connect("m14.cloudmqtt.com",11558, 60)
           #b=subscribe.simple("EMCOL", hostname="m14.cloudmqtt.com",port=11558,client_id="luciano",
                      # auth= {'username':"ouccoeks", 'password':"F-vr8zrNgD7q"} )
           #self.dadossensores=str(b.payload)
           #self.dadossensores=self.dadossensores.split(',')
           
           #self.temperatura=int(self.dadossensores[3])
           self.temperatura=1
           self.agua=1
           #self.agua=int(self.dadossensores[2])
           self.stragua=str(self.agua*10)
           self.strtemperatura= str(self.temperatura)
           self.luz=1
           self.umidade=1
           #self.umidade=int(self.dadossensores[4])
           self.strumidade=str(self.umidade)
           #self.luz=int(self.dadossensores[1])
           self.strluz=str(self.luz)
           self.strtimer=str(self.timer)
           #configurando o banco de dados sqlite
           self.date=str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%d/%m/%Y %H:%M:%S'))
           connection=sqlite3.connect('mqtttcc.db')
           c=connection.cursor()
           c.execute('CREATE TABLE IF NOT EXISTS dados(id integer,\
        keyword text,datestamp text,temperatura integer, humidadear integer,humidadeagua integer,luz integer)')
           keyword= 'estacao meteorologica com mqtt integrado'
           if self.conta<=100:
                 self.conta+=1
                 c.execute("INSERT INTO dados(id,keyword,datestamp,temperatura,humidadear,humidadeagua,luz) \
            VALUES(?,?,?,?,?,?,?)",(self.conta,keyword,self.date,self.strtemperatura,self.strumidade,self.stragua,self.strluz))
                 connection.commit()
           else:
                 self.conta2+=1
                 c.execute("""
            UPDATE dados
            SET datestamp = ?,temperatura= ?,humidadear = ?,humidadeagua = ?,luz=?
            WHERE id = ?
            """, (self.date, self.strtemperatura,self.strumidade,self.stragua,self.strluz, self.conta2))
                 connection.commit()
        
           if self.conta2>100:
                 self.conta2=0
             
            
            
           #teste.publica(self.envia)
           
       if self.mqtt==False:
           self.temperatura=1
           self.agua=1
           self.stragua=str(self.agua*10)
           self.strtemperatura= str(self.temperatura)
           self.umidade=13
           self.strumidade=str(self.umidade)
           self.luz=12
           self.strluz=str(self.luz)
           self.strtimer=str(self.timer)
           self.aviso="desligado"
       #equacao para atualizar o velocimetro
       if self.umidade<25:
           self.grafico= 90*self.umidade/25-90
       else:
           self.grafico=90*self.umidade/50
       #plotando na lista
       self.listat.append(self.xantt)
       self.listat.append(self.yantt)
       self.listat.append(self.xatualt)
       self.listat.append(self.yatualt)
       self.listau.append(self.xantu)
       self.listau.append(self.yantu)
       self.listau.append(self.xatualu)
       self.listau.append(self.yatualu)
       self.listaa.append(self.xanta)
       self.listaa.append(self.yanta)
       self.listaa.append(self.xatuala)
       self.listaa.append(self.yatuala)
       self.xatuala+=6
       self.yatuala=self.height+ self.temperatura
       self.xanta=self.xatuala
       self.yanta=self.yatuala
       self.xatualt+=6
       self.yatualt=self.height/6+self.umidade
       self.xantt=self.xatualt
       self.yantt=self.yatualt
       self.xatualu+=6
       self.yatualu=self.height/2+ self.height/10+ self.agua
       self.xantu=self.xatualu
       self.yantu=self.yatualu
       self.timer += 1
       self.tamanho+=1
       if self.mqtt==True:
           self.client.on_connect = self.on_connect
           self.client.on_message = self.on_message
           self.client.loop_forever()
    
       
       if self.timer>=2 and self.vira==True:
           self.vira=False
           self.timer=0
           self.listat=[]
           self.xantt=0
           self.xatualt=1
           self.yantt=self.height/6
           self.yatualt=self.height/6+1
           
           self.listau=[]
           self.listaa=[]
           self.xantu=0
           self.xatualu=1
           self.yantu=self.height/2+self.height/10
           self.yatualu=self.height/2+ self.height/10
           self.xanta=0
           self.xatuala=1
           self.yanta=self.height
           self.yatuala=self.height+1
       if self.timer>=30:
           self.vira=False
           self.timer=0
           self.listat=[]
           self.xantt=0
           self.xatualt=1
           #sensor de umidade
           self.yantt=self.height/6
           self.yatualt=self.height/6+1
           self.listaa=[]
           self.listau=[]
           self.xantu=0
           self.xatualu=1
           #sensor de agua
           self.yantu=self.height/2+self.height/10
           self.yatualu=self.height/2+ self.height/10
           self.xanta=0
           self.xatuala=1
           #sensor de temperatura
           self.yanta=self.height
           self.yatuala=self.height+1
      
        
       

  

class Telabanco(Screen):
    atualiza=BooleanProperty()
    servidor=StringProperty()
    aviso=StringProperty()
    def __init__(self,**kwargs):
         super(Telabanco,self).__init__(**kwargs)
         self.atualiza=False
         self.dados=""
         
    def enviadados(self):
        
        self.servidor=self.ids.dadostotais.text
        self.aviso="dados anexados,favor verificar o mqtt"
        self.dados=self.servidor
        arquivo= open('parametros.txt','w+')
        arquivo.write(self.dados)
        arquivo.close()
        

class Leitura(Screen):
    dados=StringProperty()
    def __init__(self,**kwargs):
        super(Leitura,self).__init__(**kwargs)
        self.dados=""
        self.conta=0
        connection=sqlite3.connect('mqtttcc.db')
        c=connection.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS dados(id integer,\
        keyword text,datestamp text,temperatura integer, humidadear integer,humidadeagua integer,luz integer)')
        keyword= 'estacao meteorologica com mqtt integrado'
    def exibir(self):
        self.dados=""
        self.conta+=1
        conn=sqlite3.connect('mqtttcc.db')
        c=conn.cursor()
        sql='SELECT*FROM dados WHERE id=?'
        i=0
        if self.conta==1:
            
            i=0
            for i in range(25):
                b=c.execute(sql, [(i)])
                self.dados+=str(b.fetchone())
                self.dados+="\n"
                #print(self.dados)
                i+=1
        elif self.conta==2:
            
            i=25
            for i in range(50):
                b=c.execute(sql, [(i)])
                self.dados+=str(b.fetchone())
                self.dados+="\n"
               # print(self.dados)
                i+=1
        elif self.conta==3:
            i=50
            for i in range(75):
                b=c.execute(sql, [(i)])
                self.dados+=str(b.fetchone())
                self.dados+="\n"
                #print(self.dados)
                i+=1  
        elif self.conta==4:
            i=75
            for i in range(100):
                b=c.execute(sql, [(i)])
                self.dados+=str(b.fetchone())
                self.dados+="\n"
                #print(self.dados)
                i+=1 
        elif self.conta>=5:
            self.conta=0     
        #conn=sqlite3.connect('mqtttcc.db')
        #c=conn.cursor()
        #sql='SELECT*FROM dados WHERE keyword=?'
        #for row in c.execute(sql,('estacao meteorologica com mqtt integrado',)):
             #print(row)
            #self.dados+=str(row)
             #self.dados+='\n'



class inicioapp(App):
    def build(self):
        return telaprincipal()
    
    
     
    
inicioapp().run()
    