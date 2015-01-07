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

        self.parent.title("Mipsx - GUI for gdb multiarch")
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

	menu.add_command(label="Tomar Foto", command=control.ejecutar)

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

	# Variables globales 
	self.archivoactual = "hello.s"
	self.archivoacompilar = "hello.s"
	# ip_mips = "10.0.15.232"
	self.ip_mips = "10.0.15.50"
	# ip_mips = "192.168.0.71"

	# Abrimos el archivo base
	
	# Si se finaliza el programa con click en el boton X llamamos a salir
	root.protocol("WM_DELETE_WINDOW", self.salir)


    def prox_instruccion(self):

		gdb.stdin.write('step 1\n')
		self.mostrar_en(self.paneles.mensajes, "proximo")

		self.estado()
		if self.ejecucion:
			self.memoria()
			self.registros()
			self.listado()
		
    def ejecutar(self):
		while self.ejecucion:
			self.prox_instruccion()

    def salida(self, w, findelinea):
		self.paneles.limpiar_panel(w)
				
		a = gdb.stdout.readline()
		while not findelinea in a:
			# Esto es para saber si la ejecucion termino'. 
			# TODO: Hay que quitarlo de este metodo. Donde ponerlo?
			if "No stack" in a:
				self.ejecucion = False
				# w.insert(END,'\n\nEjecucion FINALIZADA\n\n')
				self.paneles.panel_agregar(w,'\n\nEjecucion FINALIZADA\n\n')

			a = a.replace('(gdb) ', '')				
			# w.insert(END,a)		
			self.paneles.panel_agregar(w, a)
			a = gdb.stdout.readline() 		
	
    def mostrar_en(self, w, findelinea):
		gdb.stdin.write(findelinea)
		gdb.stdin.write('\r\n')
		self.salida(w, findelinea)

    def mostrar_en_depuracion(self):
		
		print "hola 3"

		

    def memoria(self):
		# Para mostrar el segmento de datos, la etiqueta memoria debe estar al principio
		gdb.stdin.write('info address memoria\n')
		gdb.stdin.write('infomemoria\n')
		a = gdb.stdout.readline()
		solicitar_seg_de_datos = ""
		while not "infomemoria" in a:
			print "a : "+a
			if "Symbol " in a:
				a = a.replace('(gdb) Symbol "memoria" is at ', '')
				a = a.replace(' in a file compiled without debugging.','')
				solicitar_seg_de_datos = "x/40xw "+a+"\n"
			a = gdb.stdout.readline()
			
		if solicitar_seg_de_datos == "":
			gdb.stdin.write('x/40xw $pc\n')
		else:
			gdb.stdin.write(solicitar_seg_de_datos)
		gdb.stdin.write('x/50xw main\n')
		gdb.stdin.write('x/128xw $sp - 128\n')
		self.mostrar_en(self.paneles.memoria, "memoria")
	

    def estado(self):
		gdb.stdin.write('info frame\n')
		self.mostrar_en(self.paneles.mensajes, "estado")


    def registros(self):
		gdb.stdin.write('info register\n')
		self.mostrar_en(self.paneles.registros, "registros")


    def listado(self):
		gdb.stdin.write('list 1,100\n')
		# gdb.stdin.write('disas main\n')
		gdb.stdin.write('disas \n')
		self.mostrar_en(self.paneles.programa, "listado")

    def compilarycargar(self):
		self.paneles.limpiar_panel(self.paneles.mensajes)
		self.paneles.panel_agregar(self.paneles.mensajes, "Compilando y Cargando ...\r\n")
		root.update_idletasks()

		# Nos liberamos del debugging actual
		gdb.stdin.write('detach \n')
		self.guardar_archivo_a_compilar()



    def abrir_en_editor(self, archivo):

		self.paneles.limpiar_panel(self.paneles.editor)
	        self.archivoactual = archivo

    def abrir(self):
		FILEOPENOPTIONS = dict(defaultextension='*.s',
                  filetypes=[('Archivo assembler','*.s'), ('Todos los archivos','*.*')])
	        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file',
				**FILEOPENOPTIONS)
	        if file != None:
			self.paneles.limpiar_paneles()
			self.abrir_en_editor(file.name)	      
 
    def guardar_archivo_a_compilar(self):
		print "hola 3"
	

    def guardar(self):
	    file = tkFileDialog.asksaveasfile(mode='w')
	    if file != None:
	    # slice off the last character from get, as an extra return is added
	        # data = editor.get('1.0', END+'-1c')
	        data = self.paneles.panel_leer(self.paneles.editor)
	        file.write(data)
	        file.close()
		self.archivoactual = file.name
                print self.archivoactual
         
    def exit_command(self):
	    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
	        root.destroy()
	 
    def acercade(self):
	    label = tkMessageBox.showinfo("Acerca de", "MIPSX - GUI for gdb multiarch\n\nEntorno de desarrollo en lenguaje assembler arquitectura MIPS\nEste programa ensabla, genera el programa ejecutable, y lo ejecuta en modo debug en una maquina MIPS real\n\nCopyright 2014 Rafael Ignacio Zurita\n\nFacultad de Informatica\nUniversidad Nacional del Comahue\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GPL v2")
		         
 
    def nuevo(self):
		self.paneles.limpiar_panel(self.paneles.editor)

    def no_hacer_nada(self):
		print "nada por hacer"

    def archivo_sin_guardar(self):

		data = self.paneles.panel_leer(self.paneles.editor)

		res = tkMessageBox.askquestion("Confirmar", "Archivo sin guardar\nEsta seguro de finalizar el programa?", icon='warning')
		if res == 'yes':
			return False

		return True

    def salir(self):

#		ip_mips = "10.0.15.50"
#		tub = Popen(['mipsx_finalizar_gdbserver.sh', ip_mips, self.PUERTOyPS], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#		streamdata = tub.communicate()[0]

		# Borrar todos los temporales

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






