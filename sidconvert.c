/*
 * Convert to the funky every-5-seconds format used by the stanford SID
 *   folks
 */
#include <stdio.h>
#include <time.h>

#define DEFAULT_RATE 5

int
main (int argc, char **argv)
{
	time_t now;
	long ut;
	double value;
	double max = -9.999e13;
	double min = 9.99e13;
	int samesec = -1;
	int rate = DEFAULT_RATE;
	
	if (argc > 1)
	{
		rate = atoi(argv[1]);
	}
		

	while (fscanf (stdin, "%ld %lf", &ut, &value) == 2)
	{
		struct tm *gmp;
		now = (time_t) ut;
		gmp = gmtime (&now);
		if (samesec != gmp->tm_sec)
		{
			samesec = gmp->tm_sec;
				
			if ((gmp->tm_sec % rate) == 0)
			{
				fprintf (stdout, "%04d-%02d-%02d %02d:%02d:%02d, %f\n",
					gmp->tm_year+1900,
					gmp->tm_mon+1,
					gmp->tm_mday,
					gmp->tm_hour,
					gmp->tm_min,
					gmp->tm_sec, value);
					if (value > max)
					{
						max = value;
					}
					if (value < min)
					{
						min = value;
					}
			}
		}
	}
	fprintf (stdout, "MAXIMUM %f\n", max);
	fprintf (stdout, "MINIMUM %f\n", min);
	return (0);
}
