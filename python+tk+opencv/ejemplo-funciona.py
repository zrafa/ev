#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
from Tkinter import *
from PIL import Image, ImageTk
import tkFileDialog

appname = "example"

class App(object):
    def __init__(self, root=None):
        if not root:
            root = Tk()
        self.root = root
        self.initUI()

    def initUI(self):
        self.root.title(appname)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        fileMenu = Menu(menubar, tearoff=0)
#        fileMenu.add_command(label="Open File", command=self.fileOpen)
#        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_command(label="File", command=self.fileOpen)
        self.canvas = Canvas(self.root)
        self.canvas.pack(side=LEFT, fill=BOTH)
        self.scrollbar_vert = Scrollbar(self.root)
        self.scrollbar_vert.pack(side=RIGHT, fill=Y)
        self.scrollbar_hor = Scrollbar(self.root)
        self.scrollbar_hor.config(orient=HORIZONTAL)
        self.scrollbar_hor.pack(side=BOTTOM, fill=X)

    def onExit(self):
        self.root.quit()

    def fileOpen(self):
#        filename = tkFileDialog.askopenfile(
#                parent=self.root,
#                mode='rb',
#                title='Choose a file',
#                filetypes=[ ( "Image files",("*.jpg", "*.jpeg", "*.png", "*.gif") ), ("All files", ("*.*"))] )
#
#        if filename == None:
#            return


	video_capture = cv2.VideoCapture(0)

	ret, frame = video_capture.read()
	cv2.imshow('Video', frame)

	params = list()
	params.append(cv2.cv.CV_IMWRITE_PXM_BINARY)
	params.append(1)

	print "hola"
	frame2 = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY) # convert to grayscale
	cv2.imwrite('cara2.pgm', frame2, params)
	cv2.imwrite('cara2.PGM', frame2, params)

	video_capture.release()
	cv2.destroyAllWindows()

	filename = 'cara2.pgm'

        self.img = Image.open(filename)
        self.photo_image = ImageTk.PhotoImage(self.img)
        self.canvas.pack_forget()
        self.canvas = Canvas(self.root, width=self.img.size[0], height=self.img.size[1])
        self.canvas.create_image(10, 10, anchor=NW, image=self.photo_image)
        self.canvas.pack(side=LEFT, fill=BOTH)
        self.canvas.config(yscrollcommand=self.scrollbar_vert.set)
        self.canvas.config(xscrollcommand=self.scrollbar_hor.set)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.scrollbar_vert.config(command=self.canvas.yview)
        self.scrollbar_hor.config(command=self.canvas.xview)

    def run(self):
        self.root.mainloop()

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = App(root)
    app.run()

if __name__ == '__main__':
    main()
