CFLAGS=-O3
PROGS=sidhandler synoptic_reader sidconvert sid_phaser
SOURCES=sidhandler.c synoptic_reader.c sidconvert.c sid_phaser.c
PYPROGS=audioSIDnetRcvr.py
GRCPROGS=audioSIDnetRcvr.grc
SCRIPTS=sidstart sidprocess sidprocess_new.awk sidship notchfilt.py sidsuite.py Makefile.sidsuite sidplot SIDsuite.doc \
	gnuradio-config.conf
all: $(PROGS)
clean:
	rm -f *.o 
	rm -f $(PROGS)
	rm -f sidsuite.tar.gz
sidhandler: sidhandler.o
synoptic_reader: synoptic_reader.o
sidconvert: sidconvert.o
tarfile: $(PROGS)
	tar czvf sidsuite.tar.gz $(SOURCES) \
	$(PYPROGS) $(GRCPROGS) $(SCRIPTS)
install: $(PROGS)
	install -D  sidhandler $(HOME)/bin/sidhandler
	install -D  synoptic_reader $(HOME)/bin/synoptic_reader
	install -D  sidconvert $(HOME)/bin/sidconvert
	install -D  sid_phaser $(HOME)/bin/sid_phaser
	install -D  sidstart $(HOME)/bin/sidstart
	install -D  sidprocess_new.awk $(HOME)/bin/sidprocess_new.awk
	install -D  sidship $(HOME)/bin/sidship
	install -D  notchfilt.py $(HOME)/bin/notchfilt.py
	install -D  sidsuite.py $(HOME)/bin/sidsuite.py
	install -D  sidprocess $(HOME)/bin/sidprocess
	install -D  audioSIDnetRcvr.py $(HOME)/bin/audioSIDnetRcvr.py
	install -D  sidplot $(HOME)/bin/sidplot
	install -D  gnuradio-config.conf $(HOME)/.gnuradio/config.conf
	echo Please see SIDsuite.doc in this directory for more information
