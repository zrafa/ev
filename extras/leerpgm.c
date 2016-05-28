
#include <ctype.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

/* MARGEN es la diferencia que debe haber entre dos colores
 * continuos para considerarse un cambio de color */
#define MARGEN 100

#define DEBUG 0

void cabecera_pgm(int f, int fout) {
	
	unsigned char c = 0;
	int n = 0;
	int i = 0;

	/* La cabecera de un pgm tiene este formato 
	 *
	 * Fuente : http://netpbm.sourceforge.net/doc/pgm.html
	 * A "magic number" for identifying the file type. A pgm image's magic number is the two characters "P5".
	 * Whitespace (blanks, TABs, CRs, LFs).
	 * A width, formatted as ASCII characters in decimal.
	 * Whitespace.
	 * A height, again in ASCII decimal.
	 * Whitespace.
	 * The maximum gray value (Maxval), again in ASCII decimal. Must be less than 65536, and more than zero.
	 * A single whitespace character (usually a newline).
	 * A raster of Height rows, in order from top to bottom. 
	 * 
	 * Por lo que tenemos 4 secciones de caracteres ASCIIs. Cada seccion separada por un whitespace.
	 */
	n = read(f, &c, 1);
	n = write(fout, &c, 1);

	for (i=0;i<=3;i++) {
		while (! isspace(c) ) {
			n = read(f, &c, 1);
			n = write(fout, &c, 1);
		}
	
		while (isspace(c) ) {
			n = read(f, &c, 1);
			n = write(fout, &c, 1);
		}

	}

}

int fila = 0;
int col = 0;
void mostrar_original(unsigned  char c) {

	printf("%i ", c);

	col++;
	if (col == 640) {
		printf("\n");
		col = 0;
		fila++;
		printf("FILA=%i\n",fila);
	}
}

int sgm[500][4];
int idx = 0;

void agregar_segmento(unsigned char flanco, int fila, int columna) {
	if (flanco == 0) /* flanco descendente, de blanco (255) paso a negro (0) */
	{
		sgm[idx][0] = fila;
		sgm[idx][1] = columna;
	} else { 	/* flanco ascendente, de negro (0) paso a blanco (255) */
		sgm[idx][2] = fila;
		sgm[idx][3] = columna;
		idx++;
	}
}

void perpendicular() {
	unsigned char encontrado = 0;
	int fi = sgm[1][0];
	int ff = 0;
	int ci = sgm[1][1];
	int cf = 0;

	int i = 48;
	int t = 0;
	int c = 0;

	int f, fout;
	int j;
	int k;
	int n;
	unsigned char ch;

/*
	f=open("salida.pgm", O_RDONLY);
	fout=open("salida2.pgm", O_RDWR | O_CREAT | O_TRUNC,  S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH);

	for (j=0;j<i;j++) {
	for (k=0;k<640;k++) {
		n = read(f, &ch, 1);
		n = write(fout, &ch, 1);
	}
	}
*/

	ff = i;
	printf ("\nANTES DE ENCONTRADO c=%i  i=%i \n", c, i);
	cf = sgm[i][1];
	printf ("\nDESPUES DE ENCONTRADO c=%i  i=%i \n", c, i);
	while (! encontrado) {

/*
		for (k=0;k<cf;k++) {
			n = read(f, &ch, 1);
			n = write(fout, &ch, 1);
		}
		n = read(f, &ch, 1);
		ch=200;
		n = write(fout, &ch, 1);
		for (k=cf+1;k<640;k++) {
			n = read(f, &ch, 1);
			n = write(fout, &ch, 1);
		}
*/

		if (sgm[i+1][1] < sgm[i][1]) {		/* si el extremo izquierdo siguiente esta a la izq */
		   t = sgm[i][1] - sgm[i+1][1];
		   if (cf+t >= sgm[i+1][3]) {	/* si el extremo derecho siguiente es inferior que el despl */
			/* NO. NO es cf+t, es ff+t y cf++. Pero tenemos que ver contra quien comparar, porque no sabemos en que i está el punto que queremos obtener de sgm para comparar con ff+t */
			t = cf+t - sgm[i+1][3];
			c = c + t;  /* t tiene que ser mayor */
			encontrado=1;
		   } else {
			c = c + t;  /* t tiene que ser mayor */
			cf = cf + t;
		   }
		
			
		} else if (sgm[i+1][1] == cf) {
			cf++;
			c++;
		}
	printf ("c=%i  i=%i t=%i sgm[i+1][1]=%i  cf=%i sgm[i][1]=%i \n", c, i, t, sgm[i+1][1], cf, sgm[i][1]);
			i++;
	}

/*
	n = read(f, &ch, 1);
	while (n>0) {
		n = write(fout, &ch, 1);
		n = read(f, &ch, 1);
	}
*/

	close(f);
	close(fout);
	printf ("c=%i  i=%i \n", c, i);
}

void mostrar_sgm() {
	int i = 0;
	for (i=0; i<480; i++)
		printf("f1: %i, c1: %i,    , f2: %i, c2: %i\n", sgm[i][0], sgm[i][1], sgm[i][2], sgm[i][3]);
}

void main (void) {
	unsigned char c = 0;	/* color leido del archivo original */
	unsigned char co = 0;	/* color output : es blanco (255) o negro (0) */
	unsigned char ca = 0; /* color anterior */
	unsigned char n = 0;
	unsigned char no = 0;
	int f, fout;

	int color_media = 0;

	// f=open("cara2.pgm", O_RDONLY);
	f=open("virtual2.pgm", O_RDONLY);
	fout=open("salida.pgm", O_RDWR | O_CREAT | O_TRUNC,  S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH);
	//fout=open("salida.pgm", O_TRUNC | O_CREAT);

	cabecera_pgm(f, fout);

	n = read(f, &c, 1);
	ca = c;

	while (n != 0) {


		color_media = color_media + c;

		#ifdef DEBUG
		mostrar_original(c);
		#endif

		co = 0;
		if ((ca-c) > MARGEN) {		/* flanco descendente */
			co = 255;
			agregar_segmento(0, fila, col);
		} else if ((c-ca) > MARGEN) {	/* flanco ascendente */
			co = 255;
			agregar_segmento(1, fila, col);
		}
		no = write(fout, &co, 1);

		ca = c;
		n = read(f, &c, 1);
			
	}

	printf("\n media color = %i \n", color_media/(640*480));

	close(f);
	close(fout);

	mostrar_sgm();
	perpendicular();
}
