ev - Analisis Digital de Diametro de Fibra UNCOMA
=================================================

Este proyecto de I+D reune los temas de hardware y software para lograr visión embebida capaz de calcular el diametro de una fibra de cabra u oveja (en micrones con una precisión de +/- 0.5 micrones). El prototipo está orientado a ser utilizado en el campo directamente, midiendo la fibra sobre el animal.

General Description
===================
This equipment uses optical and video technology to capture high resolution images of goat fibres, and
software algorithms to recognise and determine the diameters of individual fibres in the specimen.
This eliminates the need for intensive preparation of the fibre and, with a minimal amount of practice, accurate
results can be achieved quickly and easily.
The set of diameter measurements obtained during this process forms the basis from which other statistics of
interest are derived.

![alt text](extras/prototipo.png "Prototipo UNCOMA")

It lets to perform the measurement and
characterisation of fibre diameter to within one micron without removing
the fibre from the goat.
It measures, calculates, displays and records:
Mean fibre diameter,
Standard Deviation of fibre diameters,
Minimum fibre diameter, and
Maximum fibre diameter.
Coefficient of Variation of fibre
diameter, and Comfort Factor.

<img src="https://raw.githubusercontent.com/zrafa/ev/master/con-camara-y-pelos.jpg" alt="simm ram and atmega328p" width="500" height="400">


Estado: Utilizamos el algoritmo de tiempo lineal lsd para la detección de bordes.
El prototipo embebido está escrito en ANSI C, y puede ser portado a distintas plataformas de hardware facilmente.

Para compilar para mipsel usando el toolchain de JLime :

```
cd lsd_1.6
make mipsel
```

Copiar el binario lsd-mipsel y la foto del pelo que nos dieron imagenes/Pelo40X.pgm a la SIE.

Testear con :

```
./lsd-mipsel Pelo40X.pgm  salida.txt
```

Y calcula el diametro de la fibra directamente.
El algoritmo utilizado para realizacion la estadistica esta autodocumentado en el código.

Como realizar mediciones
========================

El valor medio de animales por productor es variable según la zona, y oscila entre 250 y 500 cabezas.

En cuanto a la categoría de animal a medir, mínimamente se deberían evaluar los machos (llamados "castrones"), equivalente al 4-5% del total (del "piño"). Sería bueno también medir las hembras que entren a servicio (aprox. un 70% del total).

Para una correcta medición hay que tomar 3 medidas (cuarto, costillar y paleta), y de cada lugar varias fibras (50-100).


Salida testeada en la SIE
=========================

```
Jlime$ uname -a
Linux Jlime 2.6.34-ben #39 PREEMPT Mon Apr 28 12:47:09 ART 2014 mips GNU/Linux

Jlime$ time ./lsd-mipsel Pelo40X.pgm    salida.txt

Hello World del Grosor del PELO (en pixels) = 43

real    0m 27.19s
user    0m 27.02s
sys     0m 0.15s
```


En la SIE la estadistica indica que la media es de 43 pixels.

pelosvision.py
==============

Este es un prototipo para "imitar" el comportamiento del wool view.

Requisitos - Instalar :
```
apt-get install imagemagick python-opencv python-tk python-pil python-pil.imagetk build-essential xdotool
```

Como Testear el código
----------------------

```
git clone https://github.com/zrafa/ev.git
cd ev
# Compilamos lsd
cd lsd_1.6/
make all
cd ..
# Probamos el prototipo con la interfaz gráfica en python
cd python+tk+opencv/
python pelosvision.py


```



