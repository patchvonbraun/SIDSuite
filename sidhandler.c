#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define NCHANS 12
#define NDATA  8
FILE *chans[NCHANS];
FILE *ichans[NCHANS];
float inbuf[NCHANS*NDATA];
int lastday = -1;
int
main (int argc, char **argv)
{
	int i;
	int j;
	time_t now;
	struct tm *gmp;
	
	for (i = 0; i < NCHANS; i++)
	{
		ichans[i] = NULL;
	}

	for (i = 1; i < argc; i++)
	{
		int fd;
		if ((fd = open (argv[i], O_RDONLY|O_NONBLOCK)) < 0)
		{
			perror ("opening input file\n");
			exit (0);
		}
		ichans[i-1] = fdopen (fd, "r");
		if (ichans[i-1] == NULL)
		{
			perror ("reopening fd as FP\n");
			exit (0);
		}
	}
	while (1)
	{
		int choccupied;
		
		time (&now);
		gmp = gmtime (&now);
		if (gmp->tm_wday != lastday)
		{
			char filename[128];

			/*
			 * New files
			 */
			lastday = gmp->tm_wday;
			for (i = 0; i < NCHANS; i++)
			{
				if (ichans[i] != NULL)
				{
					if (chans[i] != NULL)
					{
						fclose (chans[i]);
					}
					sprintf (filename, "chan%d-%04d%02d%02d.dat", i+1,
						gmp->tm_year+1900,
						gmp->tm_mon+1,
						gmp->tm_mday);
					chans[i] = fopen (filename, "a");
				}
			}
		}
		choccupied = 0;
		for (i = 0; i < NCHANS; i++)
		{
			if (ichans[i] != NULL)
			{
				if (fread (inbuf, 1*sizeof(float), 1, ichans[i]) > 0)
				{
					for (j = 0; j < 1; j++)
					{
						fprintf (chans[i], "%d %f\n", (int)now, inbuf[j]);
					}
					fflush (chans[i]);
					choccupied = i+1;
				}
			}
		}
		if (choccupied == 0)
		{
			usleep (100000);
		}
	}
}
