
#include <ctype.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>


unsigned char pixels[640*480];

void cabecera_pgm(int f) {
	
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

	for (i=0;i<=3;i++) {
		if (c == '#') {
			while (! isspace(c) ) {
				n = read(f, &c, 1);
			}
			while (isspace(c) ) {
				n = read(f, &c, 1);
			}
		}

		while (! isspace(c) ) {
			n = read(f, &c, 1);
		}
		while (isspace(c) ) {
			n = read(f, &c, 1);
		}

	}
	pixels[0]=c;

}


void cargar_pixels(const char *imagen) {

	int f, n;
	unsigned char c;

	f=open(imagen, O_RDONLY);

	cabecera_pgm(f);
	n = read(f, &c, 1);

	int i = 1;

	while (n != 0) {


		pixels[i] = c;
		i++;
		n = read(f, &c, 1);
	}

	close(f);

}

