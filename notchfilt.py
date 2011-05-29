#
# Notch-filter generator for filtinter out the harmonics of the local
#   power-line frequency
#
# Marcus Leech, Science Radio Laboratories, Inc.
#
import numpy
def notch_taps(rate,line_freq,max_harmonic):
	resolution=10
	if (line_freq == 50):
		resolution=10
	harms=[]
	for i in range(1,max_harmonic):
		harms.append(int(i*line_freq))
	ttaps=[]
	for i in range(0,int(rate/resolution)):
		freq=int(i*resolution)
		if (freq in harms):
			ttaps.append(complex(0.0,0.0))
		else:
			ttaps.append(complex(0.0,1.0))

	return(numpy.fft.ifft(ttaps))
	
