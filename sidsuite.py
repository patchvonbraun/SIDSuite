#
# Variables saver for SIDsuite
#
# Marcus Leech, Science Radio Laboratories, Inc.
#
import os
def variables(fn,c1,c2,c3,c4,c5,c6,integ,cbw,demod,gain,width,start):
	file=open(fn, "w")
	file.write("BANDWIDTH="+str(cbw)+"\n")
	file.write("INTEG="+str(integ)+"\n")
	file.write("F0="+str(c1)+"\n")
	file.write("F1="+str(c2)+"\n")
	file.write("F2="+str(c3)+"\n")
	file.write("F3="+str(c4)+"\n")
	file.write("F4="+str(c5)+"\n")
	file.write("F5="+str(c6)+"\n")
	file.write("AWID="+str(width)+"\n")
	file.write("ASTART="+str(start)+"\n")
	file.write("GAIN="+str(gain)+"\n")
	file.close()
	return 0
