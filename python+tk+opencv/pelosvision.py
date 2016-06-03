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

        self.parent.title("Analisis Digital de Diametro de Fibra UNCOMA")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

	# Para expandir cuando las ventanas cambian de tamao 
	for i in range(3):
		self.columnconfigure(i, weight=1)
	for i in range(20):
		self.rowconfigure(i, weight=1)

        lbl = Label(self, text="Valor máximo de aceptación de diametro (en pixels)")
        lbl.grid(row=13,column=0, sticky=W, pady=4, padx=5) 

	self.limite = Entry(self)
	self.limite.grid(row=13, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
	self.limite.delete(0, END)
	self.limite.insert(0, "80")

	self.lbl_estadistica = Text(self, height=6, width=60)
        self.lbl_estadistica.grid(row=1,column=1, sticky=W, pady=1, padx=5) 
	self.lbl_estadistica.insert(END, "Hola que tal")
        lbl = Label(self, text="Estadistica obtenida :")
        lbl.grid(row=1,column=0, sticky=W, pady=1, padx=5) 
        lbl = Label(self, text="Diametro obtenido (MEDIA, en pixels)")
        lbl.grid(row=2,column=0, sticky=W, pady=1, padx=5) 
	self.grosor = Entry(self)
	self.grosor.grid(row=2, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
        
        lbl = Label(self, text="Diametro obtenido (MEDIA, en micrones)")
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
	self.micron.insert(0, "0.9743")

        lbl = Label(self, text="Valor deseado en la Secuencia de Fotos")
        lbl.grid(row=11,column=0, sticky=W, pady=1, padx=5) 
	self.secuencia = Entry(self)
	self.secuencia.grid(row=11, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
	self.secuencia.delete(0, END)
	self.secuencia.insert(0, "1")

        lbl = Label(self, text="Valor minimo de aceptacion de diametro (en pixels)")
        lbl.grid(row=12,column=0, sticky=W, pady=1, padx=5) 
	self.minimo = Entry(self)
	self.minimo.grid(row=12, column=1, columnspan=1, padx=1, sticky=E+W+S+N)
	self.minimo.delete(0, END)
	self.minimo.insert(0, "10")

	menu = Menu(root)
	root.config(menu=menu)
	filemenu = Menu(menu)

	menu.add_command(label="    Tomar Foto    ", command=control.tomarFotoConPrevia)
	menu.add_command(label="    Tomar Secuencia de Fotos    ", command=control.tomarSecuencia)

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
		# output = Popen(["../lsd_1.6/lsd", "-T", self.minimo.get(), "-t", self.limite.get(), "-a", "100", "-P", "salida.eps", filename, "salida.txt"], stdout=PIPE).communicate()[0]
		output = Popen(["../lsd_1.6/lsd", "-T", self.minimo.get(), "-t", self.limite.get(), "-P", "salida.eps", filename, "salida.txt"], stdout=PIPE).communicate()[0]
		output2 = Popen(["./backup-de-la-foto.sh"], ).communicate()[0]
		output = output.replace('Grosor del PELO en pixels : ', '')
		self.grosor.delete(0, END)
		self.grosor.insert(0, output)
		self.grosormicron.delete(0, END)
		self.grosormicron.insert(0, float(output)*float(self.micron.get()))
		print output
		output = Popen(["./procesar.sh", self.minimo.get(), self.limite.get(), filename ], stdout=PIPE).communicate()[0]
		self.lbl_estadistica.delete('1.0', END)
		self.lbl_estadistica.insert('1.0', "\n")
		self.lbl_estadistica.insert('2.0', output)

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

	filename = 'unpelo.pgm'

	self.paneles.mostrarFoto(filename)
	self.paneles.calcularGrosor(filename)
	self.paneles.mostrarFoto2(filename)

    def key(self, event):
        print "pressed", repr(event.char)
        if event.keysym == '1':
                self.tomarFoto(True)
        elif event.keysym == '3':
                cam = self.paneles.camara.get()
                self.paneles.camara.delete(0, END)
                if cam == "0":
                        self.paneles.camara.insert(0, "1")
                elif cam == "1":
                        self.paneles.camara.insert(0, "2")
                else:
                        self.paneles.camara.insert(0, "0")

        elif event.keysym == '4':
                quit()


		

    def tomarSecuencia(self):
	media_general = 0
	for i in range(int(self.paneles.secuencia.get())):
		self.tomarFoto(False)
		media_general = media_general + int(self.paneles.grosor.get())

	media_general = media_general / int(self.paneles.secuencia.get())
	self.paneles.grosor.delete(0, END)
	self.paneles.grosor.insert(0, media_general)


    def tomarFotoConPrevia(self):
	self.tomarFoto(True)

    def tomarFoto(self, previa):

	# Bloque : Tomamos la foto desde la web cam y la grabamos en formato PGM
	# video_capture = cv2.VideoCapture(0)
	video_capture = cv2.VideoCapture(int(self.paneles.camara.get()))

	#cap = cv2.VideoCapture(0)

        enfocado = False
	while(previa):
	    # Capture frame-by-frame
	    ret, frame = video_capture.read()

	    # Our operations on the frame come here
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    cv2.imshow('Video de enfoque y disparo - presione la tecla "7" para tomar una foto',gray)
            if not enfocado:
                if cv2.waitKey(5):
                        salida = Popen(["./fw.sh"], stdout=PIPE).communicate()[0]
                        enfocado = True

	    if cv2.waitKey(1) & 0xFF == ord('7'):
	    	ret, frame = video_capture.read()
       		break

	# When everything done, release the capture
	# cap.release()
	# cv2.destroyAllWindows()
	cv2.destroyWindow('Video de enfoque y disparo - presione la tecla "7" para tomar una foto')

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
        salida = Popen(["./mw.sh"], stdout=PIPE).communicate()[0]

 
    def acercade(self):
	    label = tkMessageBox.showinfo("Acerca de", "Analisis Digital de Diametro de Fibra UNCOMA\n\nEste programa en Python Tk y Opencv toma una foto desde una camara usb, la guarda en formato PGM, la analiza con lsd y calcula el diametro (media) de fibras en la foto. Presenta la foto capturada y sus resultados. \n\nCopyright (C) 2015 Rafael Ignacio Zurita y Rodolfo del Castillo\n\nFacultad de Informatica\nUniversidad Nacional del Comahue\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GPL v2")
		         
 
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
	root.bind_all('<Key>', app.key)
	main()  


