
#include <ctype.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#ifndef _LEERPGM_H
#define _LEERPGM_H

void cabecera_pgm(int f);
	
void cargar_pixels(const char *imagen);

#endif
