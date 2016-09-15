#!/bin/bash

../lsd_1.6/lsd -T $1 -t $2 -P salida.eps $3 salida.txt 2>&1 | egrep -i "varianza|desviacion|mediciones" | sed -e "s/\t//g"

