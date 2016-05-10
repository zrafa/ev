
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>


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

void main (void) {
	unsigned char c = 0;
	unsigned char co = 0;
	unsigned char ca = 0; /* color anterior */
	unsigned char n = 0;
	unsigned char no = 0;
	int f, fout;
	int col = 0;
	int fila = 0;

	int color_media = 0;

	// f=open("cara2.pgm", O_RDONLY);
	f=open("virtual.pgm", O_RDONLY);
	fout=open("salida.pgm", O_RDWR | O_CREAT | O_TRUNC,  S_IRUSR | S_IRGRP | S_IROTH);

	cabecera_pgm(f, fout);

	n = read(f, &c, 1);
	n = write(fout, &c, 1);

	printf("%i ", c);
	while (n != 0) {
		ca = c;
		n = read(f, &c, 1);


		color_media = color_media + c;

		printf("%i ", c);
		col++;
		if (col == 640) {
			printf("\n");
			col = 0;
			fila++;
			printf("FILA=%i\n",fila);
		}
// if (c>200) {
if (((c-ca)>15) || ((ca-c)>15)) {
	co = 255;
	no = write(fout, &co, 1);
			
} else {
	co = 0;
	no = write(fout, &co, 1);
}

			
	}
	printf("\n media color = %i \n", color_media/(640*480));
	close(f);
	close(fout);





}
