BEGIN { c=1
        BTIM=120
        SRATE=8
        BSZ=SRATE*BTIM
	FRAC=5
      }
/./ {if (init <= 0)
     {
         BSZ=SRATE*BTIM
         init = 1
     }
     samples++
     if (samples >= SRATE)
     {
         samples = 0
         seconds += 1
     }
     seconds = $1
     if ((ST_TIME > 0 && seconds < ST_TIME) || (EN_TIME > 0 && seconds > EN_TIME))
     {
		next
	 }
	c1array[c] = $2
        c++
	if (c >= BSZ)
        {
            c = 1
            asort(c1array)
	    c1avg = 0
            interval=(BSZ-(BSZ/FRAC))
            interval -= (BSZ/FRAC)
            for (i = BSZ/FRAC; i < BSZ-(BSZ/FRAC); i++)
            {
                c1avg += c1array[i]
            }
            printf ("%d %f\n", (seconds)-(BTIM/2), c1avg/interval)
         }
            
    }
