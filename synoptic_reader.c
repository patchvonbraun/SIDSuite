#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <time.h>
#include <sys/time.h>
#define DEFAULT_SIZE 96000
FILE *output;
int lastday = -1;
int
main (int argc, char **argv)
{
	FILE *input;
	time_t now;
	struct tm *gmp;
	float *inbuf;
	int insize = DEFAULT_SIZE;
	int inbufsz;

	if ((input = fopen (argv[1], "r")) == NULL)
	{
		perror ("Opening input file\n");
		exit (0);
	}
	if (argc > 2)
	{
		insize = atoi(argv[2]);
	}
	inbufsz = insize * 2 * sizeof(float);
	inbuf = (float *)malloc (inbufsz);
	while (fread ((void *)inbuf, inbufsz, 1, input) > 0)
	{
		time (&now);
		gmp = gmtime (&now);
		if (gmp->tm_wday != lastday)
		{
			char filename[128];

			/*
			 * New files
			 */
			lastday = gmp->tm_wday;
			if (output != NULL)
			{
				fclose (output);
			}
			sprintf (filename, "synoptic-%04d%02d%02d.dat",
					gmp->tm_year+1900,
					gmp->tm_mon+1,
					gmp->tm_mday);
			output = fopen (filename, "a");
		}
		fwrite (inbuf, inbufsz, 1, output);
		fflush (output);
	}
	return (0);
}
