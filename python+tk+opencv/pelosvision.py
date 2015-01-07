#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Autor original del ejemplo de una aplicacion Tk: Jan Bodnar
last modified: December 2010
website: www.zetcode.com

Modificado y ampliado para ser una GUI de GDB para MIPS. 
(C) 2014 - Rafael Ignacio Zurita <rafa@fi.uncoma.edu.ar>

Lea el archivo README.md para conocer la licencia de este programa.
"""

import time
import sys
import random

from subprocess import Popen, PIPE, STDOUT

from Tkinter import *
from ttk import Frame, Button, Label, Style

# Para extrar el nombre de archivo sin ruta
import ntpath

from ScrolledText import *
import tkFileDialog
import tkMessageBox

class MipsxTkGui(Frame):
  


    def __init__(self, parent, control):

      	Frame.__init__(self, parent)   
         
       	self.parent = parent

        self.parent.title("Hello World para calcular grosor de pelo")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

	# Para expandir cuando las ventanas cambian de tamao 
	for i in range(3):
		self.columnconfigure(i, weight=1)
	for i in range(20):
		self.rowconfigure(i, weight=1)

        lbl = Label(self, text="Foto")
        lbl.grid(row=3,column=0, sticky=W, pady=4, padx=5)
        
        self.registros = Text(self,height=12,width=40)
        self.registros.grid(row=4, column=0, columnspan=1, rowspan=5, sticky=E+W+S+N)
        
        lbl = Label(self, text="Foto 2")
        lbl.grid(row=3,column=1, sticky=W, pady=4, padx=5)
        
        self.foto2 = Text(self,height=12,width=40)
	self.foto2.grid(row=4, column=1, sticky=E+W+S+N)
        
        lbl = Label(self, text="Numero de la Video Camara")
        lbl.grid(row=2,column=0, sticky=W, pady=1, padx=5) 

	self.camara = Entry(self)
	self.camara.grid(row=2, column=1, columnspan=1, padx=1, sticky=E+W+S+N)


        lbl = Label(self, text="Limite de grosor")
        lbl.grid(row=1,column=0, sticky=W, pady=4, padx=5) 
     
	self.editor = Entry(self)
	self.editor.grid(row=1, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
        
      
	menu = Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)

	menu.add_command(label="Tomar Foto", command=control.salir)

	helpmenu = Menu(menu)
	menu.add_cascade(label="Ayuda", menu=helpmenu)
	helpmenu.add_command(label="Acerca de...", command=control.acercade)
	menu.add_command(label="Salir", command=control.salir)

    def limpiar_panel(self, panel):
		panel.delete('1.0',END)

    def panel_agregar(self, panel, contenido):
		panel.insert(END, contenido)

    def panel_leer(self, panel):
		return panel.get('1.0', END+'-1c')

    def mostrar_en_area(self, area):
		print "hola"

    # Al abrir un archivo deseamos tener un area de trabajo cero
    def limpiar_paneles(self):
		self.mensajes.delete('1.0',END)
		self.memoria.delete('1.0',END)
		self.programa.delete('1.0',END)
		self.registros.delete('1.0',END)



class MipsxControl(Frame):


    def __init__(self, parent):

    	self.paneles = MipsxTkGui(parent, self)

	self.ejecucion = False

	
	# Si se finaliza el programa con click en el boton X llamamos a salir
	root.protocol("WM_DELETE_WINDOW", self.salir)


		

		

 
    def acercade(self):
	    label = tkMessageBox.showinfo("Acerca de", "Hello World para calcular grosor de pelo\n\nEste programa en Python Tk y Opencv toma una foto desde una camara usb, la guarda en formato PGM, la analiza con lsd y calcula el grosor (media) de los pelos en la foto. Muestra la foto tomada y la resultante con los calculos. \n\nCopyright (C) 2015 Rafael Ignacio Zurita y Rodolfo del Castillo\n\nFacultad de Informatica\nUniversidad Nacional del Comahue\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GPL v2")
		         
 
    def no_hacer_nada(self):
		print "nada por hacer"

    def salir(self):


		quit()


        


 
 

def main():
  
	root.mainloop()  



if __name__ == '__main__':
	root = Tk()    

	# Para expandir cuando las ventanas cambian de tamao 
	root.columnconfigure(0,weight=1)
	root.rowconfigure(0, weight=1)

    	app = MipsxControl(root)
	main()  






