#!/bin/bash
SALIDA=/tmp/$RANDOM
SALIDA_VARIANZA=/tmp/$RANDOM
for i in `find $@ -type f`;do
    printf "\n\n Archivo $i:\n" >> $SALIDA_VARIANZA
    ../lsd_1.6/lsd -T 10 -t 50  -P salida.eps  $i salida.txt >> $SALIDA_VARIANZA 2>&1

    ../lsd_1.6/lsd -T 10 -t 50  -P salida.eps  $i salida.txt
done | tee $SALIDA | awk 'BEGIN{sum = 0}{sum = sum + $NF; print "Intermedio "NR" "sum/NR*1.0325}END{print sum/NR}'

cat $SALIDA_VARIANZA | egrep -i "varianza|desviacion|mediciones|Archivo|^$" > ${SALIDA_VARIANZA}.res ; rm $SALIDA_VARIANZA
echo "El listado intermedio en $SALIDA"
echo "La estadistica de cada medicion en ${SALIDA_VARIANZA}.res"
