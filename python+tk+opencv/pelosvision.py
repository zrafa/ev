#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PelosVision - Calcula el grosor (media) de pelos en una foto
(C) 2014 - Rafael Ignacio Zurita <rafa@fi.uncoma.edu.ar>

Lea el archivo README.md para conocer la licencia de este programa.
"""

import cv2
from Tkinter import *
from PIL import Image, ImageTk

import time
import sys
import random

from subprocess import Popen, PIPE, STDOUT

from ttk import Frame, Button, Label, Style

# Para extrar el nombre de archivo sin ruta
import ntpath

from ScrolledText import *
import tkFileDialog
import tkMessageBox
import ttk

class PelosVisionTkGui(Frame):

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

        lbl = Label(self, text="Limite de grosor máximo (en pixels)")
        lbl.grid(row=1,column=0, sticky=W, pady=4, padx=5) 

	self.limite = Entry(self)
	self.limite.grid(row=1, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
	self.limite.delete(0, END)
	self.limite.insert(0, "70")

        lbl = Label(self, text="Grosor obtenido (en pixels)")
        lbl.grid(row=2,column=0, sticky=W, pady=1, padx=5) 
	self.grosor = Entry(self)
	self.grosor.grid(row=2, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
        
        lbl = Label(self, text="Grosor obtenido (en micrones)")
        lbl.grid(row=3,column=0, sticky=W, pady=1, padx=5) 
	self.grosormicron = Entry(self)
	self.grosormicron.grid(row=3, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
       
	lbl = ttk.Separator(self,orient=HORIZONTAL).grid(row=4, columnspan=2, sticky="ew")

        lbl = Label(self, text="Foto")
        lbl.grid(row=5,column=0, sticky=W, pady=4, padx=5)
        self.foto1 = Canvas(self)
        self.foto1.grid(row=6, column=0, sticky=E+W+S+N)
        
        lbl = Label(self, text="Representacion del Analisis")
        lbl.grid(row=5,column=1, sticky=W, pady=4, padx=5)
        self.foto2 = Canvas(self)
        self.foto2.grid(row=6, column=1, sticky=E+W+S+N)
        
	lbl = ttk.Separator(self,orient=HORIZONTAL).grid(row=7, columnspan=2, sticky="ew")

        lbl = Label(self, text="Opciones Avanzadas : ")
        lbl.grid(row=8,column=0, sticky=W, pady=1, padx=5) 

        lbl = Label(self, text="Numero de la Video Camara")
        lbl.grid(row=9,column=0, sticky=W, pady=1, padx=5) 
	self.camara = Entry(self)
	self.camara.grid(row=9, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
	self.camara.delete(0, END)
	self.camara.insert(0, "0")

        lbl = Label(self, text="Calibracion 1 pixel = (micrones)")
        lbl.grid(row=10,column=0, sticky=W, pady=1, padx=5) 
	self.micron = Entry(self)
	self.micron.grid(row=10, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
	self.micron.delete(0, END)
	self.micron.insert(0, "0.5")

	menu = Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)

	menu.add_command(label="    Tomar Foto    ", command=control.tomarFoto)

	helpmenu = Menu(menu)
	menu.add_cascade(label="Ayuda", menu=helpmenu)
	helpmenu.add_command(label="Acerca de...", command=control.acercade)
	menu.add_command(label="Salir", command=control.salir)


    def mostrarFoto(self,filename):

	self.img = Image.open(filename)
        resized = self.img.resize((400, 300),Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(resized)
        self.foto1.pack_forget()
        # self.foto1 = Canvas(self, width=self.img.size[0], height=self.img.size[1])
        self.foto1 = Canvas(self, width=400, height=300)
        self.foto1.create_image(10, 10, anchor=NW, image=self.photo_image)
        self.foto1.grid(row=6, column=0, sticky=E+W+S+N)

    def calcularGrosor(self,filename):
		# ../lsd_1.6/lsd -P salida.eps imagenes/Pelo40X.pgm  salida.txt
		output = Popen(["../lsd_1.6/lsd", "-P", "salida.eps", filename, "salida.txt"], stdout=PIPE).communicate()[0]
		output = output.replace('Grosor del PELO en pixels : ', '')
		self.grosor.delete(0, END)
		self.grosor.insert(0, output)
		self.grosormicron.delete(0, END)
		self.grosormicron.insert(0, float(output)*float(self.micron.get()))
		print output

    def mostrarFoto2(self,filename):
		# Hay que ejecutar para hacer merge de los EPS generados :
		# convert salida.ps grosordelpelo.eps -layers merge salida2.png
		output = Popen(["convert", "salida.eps", "grosordelpelo.eps", "-layers", "merge", "salida2.png"], stdout=PIPE).communicate()[0]
		# Mostramos la foto 2
		self.img2 = Image.open("salida2.png")
        	resized2 = self.img2.resize((400, 300),Image.ANTIALIAS)
        	self.photo_image2 = ImageTk.PhotoImage(resized2)
        	self.foto2.pack_forget()
        	self.foto2 = Canvas(self, width=400, height=300)
        	self.foto2.create_image(10, 10, anchor=NW, image=self.photo_image2)
        	self.foto2.grid(row=6, column=1, sticky=E+W+S+N)


class PelosVisionControl(Frame):


    def __init__(self, parent):

    	self.paneles = PelosVisionTkGui(parent, self)

	self.ejecucion = False

	
	# Si se finaliza el programa con click en el boton X llamamos a salir
	root.protocol("WM_DELETE_WINDOW", self.salir)

		

    def tomarFoto(self):

	# Bloque : Tomamos la foto desde la web cam y la grabamos en formato PGM
	# video_capture = cv2.VideoCapture(0)
	video_capture = cv2.VideoCapture(int(self.paneles.camara.get()))

	#cap = cv2.VideoCapture(0)

	while(True):
	    # Capture frame-by-frame
	    ret, frame = video_capture.read()

	    # Our operations on the frame come here
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    cv2.imshow('Video de enfoque y disparo - presione la tecla "s" para tomar una foto',gray)
	    if cv2.waitKey(1) & 0xFF == ord('s'):
	    	ret, frame = video_capture.read()
       		break

	# When everything done, release the capture
	# cap.release()
	# cv2.destroyAllWindows()
	cv2.destroyWindow('Video de enfoque y disparo - presione la tecla "s" para tomar una foto')

	ret, frame = video_capture.read()
	#cv2.imshow('Video', frame)

	params = list()
	params.append(cv2.cv.CV_IMWRITE_PXM_BINARY)
	params.append(1)

	frame2 = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY) # convert to grayscale
	cv2.imwrite('cara2.pgm', frame2, params)
	cv2.imwrite('cara2.PGM', frame2, params)

	video_capture.release()
	cv2.destroyAllWindows()
	# Fin de Tomamos la foto desde la web cam y la grabamos en formato PGM

	filename = 'cara2.pgm'

	self.paneles.mostrarFoto(filename)
	self.paneles.calcularGrosor(filename)
	self.paneles.mostrarFoto2(filename)

 
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

    	app = PelosVisionControl(root)
	main()  


