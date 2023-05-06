#   the default target
all:
	apxs -Wc,-D_FORTIFY_SOURCE=0 -c mod_pwnable.c

#   install the shared object file into Apache 
install:
	cp .libs/mod_pwnable.so /usr/local/apache2/modules/

#   cleanup
clean:
	-rm -f mod_pwnable.o mod_pwnable.lo mod_pwnable.slo mod_pwnable.la 

#   simple test
test: reload
	lynx -mime_header http://localhost/ctf
