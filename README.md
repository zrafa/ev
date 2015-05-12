ev - pruebas para embedded vision
=================================

Este proyecto de I+D reune los temas visión embebida en una aplicación 
para calcular el grosor de pelos en micrones.


<img src="https://raw.githubusercontent.com/zrafa/ev/master/con-camara-y-pelos.jpg" alt="simm ram and atmega328p" width="500" height="400">


Estado: Utilizamos un programa llamado lsd. Con el programa lsd obtenemos los bordes del pelo en "segmentitos".
Usando esos segmentitos hemos agregamos una funcion que calcula el grosor del pelo de manera básica.

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

Y nos calcula el grosor del pelo basicamente.
El algoritmo utilizado para calcularlo con los segmentitos está en el archivo lsd_1.6/matematicas.txt. Y el codigo son dos funciones llamadas pendientes() y grosor(), que fueron agregadas al archivo fuente lsd_1.6/lsd-cmd.c 


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


En la SIE calcula que el grosor del pelo que nos dieron es de 43 pixels.

pelosvision.py
==============

Este es un prototipo para "imitar" el comportamiento del wool view.

Requisitos - Instalar :
```
apt-get install imagemagick python-opencv python-tk python-pil python-pil.imagetk build-essential
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



