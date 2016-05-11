
#include <ctype.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

/* MARGEN es la diferencia que debe haber entre dos colores
 * continuos para considerarse un cambio de color */
#define MARGEN 15

// #define DEBUG 0

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

void main (void) {
	unsigned char c = 0;	/* color leido del archivo original */
	unsigned char co = 0;	/* color output : es blanco (255) o negro (0) */
	unsigned char ca = 0; /* color anterior */
	unsigned char n = 0;
	unsigned char no = 0;
	int f, fout;

	int color_media = 0;

	// f=open("cara2.pgm", O_RDONLY);
	f=open("virtual.pgm", O_RDONLY);
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
		if (((c-ca)>MARGEN) || ((ca-c)>MARGEN)) {
			co = 255;
		}
		no = write(fout, &co, 1);

		ca = c;
		n = read(f, &c, 1);
			
	}

	printf("\n media color = %i \n", color_media/(640*480));

	close(f);
	close(fout);

}
