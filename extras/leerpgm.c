
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

void cabecera_pgm(int f, int fout) {
	
	unsigned char c = 0;
	int n = 0;

	n = read(f, &c, 1);
	n = write(fout, &c, 1);

	while (! isspace(c) ) {
		n = read(f, &c, 1);
		n = write(fout, &c, 1);
	}

	while (isspace(c) ) {
		n = read(f, &c, 1);
		n = write(fout, &c, 1);
	}

	while (! isspace(c) ) {
		n = read(f, &c, 1);
		n = write(fout, &c, 1);
	}

	while (isspace(c) ) {
		n = read(f, &c, 1);
		n = write(fout, &c, 1);
	}

	while (! isspace(c) ) {
		n = read(f, &c, 1);
		n = write(fout, &c, 1);
	}

	while (isspace(c) ) {
		n = read(f, &c, 1);
		n = write(fout, &c, 1);
	}

	while (! isspace(c) ) {
		n = read(f, &c, 1);
		n = write(fout, &c, 1);
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

	f=open("cara2.pgm", O_RDONLY);
	//fout=open("salida.pgm", O_RDWR | O_CREAT | O_TRUNC);
	fout=open("salida.pgm", O_RDWR);

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
