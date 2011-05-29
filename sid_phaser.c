#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <time.h>
#include <sys/time.h>
#define NCHANS 8
#define NDATA  100
FILE *pos_chan, *neg_chan;
FILE *ichan;
float inbuf[NDATA];
int lastday = -1;

#define TODEGREES 180.0/3.14159265358

int
main (int argc, char **argv)
{
	int j;
	time_t now;
	struct tm *gmp;
	
	if ((ichan = fopen (argv[1], "r")) == NULL)
	{
		perror ("opening input");
		exit (0);
	}
	while (1)
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
			if (pos_chan != NULL)
			{
				fclose (pos_chan);
				fclose (neg_chan);
			}
			sprintf (filename, "phase_pos-%04d%02d%02d.dat",
						gmp->tm_year+1900,
						gmp->tm_mon+1,
						gmp->tm_mday);
			pos_chan = fopen (filename, "a");
			sprintf (filename, "phase_neg-%04d%02d%02d.dat",
						gmp->tm_year+1900,
						gmp->tm_mon+1,
						gmp->tm_mday);
			neg_chan = fopen (filename, "a");
		}

		if (fread (inbuf, NDATA*sizeof(float), 1, ichan) > 0)
		{
			float nc, pc;
			int ncount, pcount;
			
			nc = pc = 0.0;
			ncount = pcount = 0;
			for (j = 0; j < NDATA; j++)
			{
				if (inbuf[j] > 0.05)
				{
					pc += inbuf[j];
					pcount++;
				}
				if (inbuf[j] < -0.05)
				{
					nc += inbuf[j];
					ncount++;
				}
			}
			fprintf (neg_chan, "%d %f\n", (int)now, (nc/(float)ncount)*TODEGREES);
			fprintf (pos_chan, "%d %f\n", (int)now, (pc/(float)pcount)*TODEGREES);
			fflush (neg_chan);
			fflush (pos_chan);
		}
		else
		{
			exit (0);
		}
	}
}

