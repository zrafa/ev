ev - pruebas para embedded vision
=================================

Este programita es un Hello World para calcular el grosor de un pelo.

Utilizamos un programa llamado lsd. Con el programa lsd obtenemos los bordes del pelo en "segmentitos".
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
