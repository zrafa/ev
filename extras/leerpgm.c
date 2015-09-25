
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>

void main (void) {
	unsigned char c = 0;
	unsigned char ca = 0; /* color anterior */
	unsigned char n = 0;
	int f;
	int col = 0;
	int fila = 0;

	int color_media = 0;

/* Creamos un archivo eps para anexar */
  FILE * eps;
        char *filename = "grosordelpelo.eps";

  /* open file */
  if( strcmp(filename,"-") == 0 ) eps = stdout;
  else eps = fopen(filename,"w");
  if( eps == NULL ) error("Error: unable to open EPS output file.");

  /* write EPS header */
  fprintf(eps,"%%!PS-Adobe-3.0 EPSF-3.0\n");
  fprintf(eps,"%%%%BoundingBox: 0 0 %d %d\n",640,480);
  fprintf(eps,"%%%%Creator: LSD, Line Segment Detector\n");
  fprintf(eps,"%%%%Title: (%s)\n",filename);
  fprintf(eps,"%%%%EndComments\n");

/* Fin de Creamos un archivo eps para anexar */




	f=open("cara2.pgm", O_RDONLY);
	n = read(f, &c, 1);
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
if (((c-ca)>25) || ((ca-c)>25)) {
/* Agregamos datos al archivo grosordelpelo.eps */
      fprintf( eps,"newpath %f %f moveto %f %f lineto 1 0 0 setrgbcolor 4  setlinewidth stroke\n",
(double) col,
(double) 480-fila,
               (double) col+1,
(double) 480-fila
                 );
/* Fin de Agregamos datos al archivo grosordelpelo.eps */
			
}

			
	}
	printf("\n media color = %i \n", color_media/(640*480));
	close(f);




/* Cerramos al archivo grosordelpelo.eps */
  fprintf(eps,"showpage\n");
  fprintf(eps,"%%%%EOF\n");
  if( eps != stdout && fclose(eps) == EOF )
    error("Error: unable to close file while writing EPS file.");
/* Fin de Cerramos al archivo grosordelpelo.eps */


}
