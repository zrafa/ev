#!/bin/bash

DIR_RAND=/tmp/$RANDOM

if [[ $# -lt 1 ]] ; then
	echo "Uso : procesar_imagenes.sh dir1 [dir2] [dir3] .."
	exit 1
fi

mkdir $DIR_RAND

for i in $(find $@ -type f) ; do 
	cp $i unpelo.pgm
	python pelosvision.py &  
	sleep 5 
	gnome-screenshot -w -f /tmp/salida.jpg
	mv /tmp/salida.jpg ${DIR_RAND}/$(basename $i).procesado.jpg
	kill $!
done

echo "Capturas del procesamiento en $DIR_RAND"
