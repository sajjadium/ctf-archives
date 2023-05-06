
.PHONY: all
all: crypto_sign.tar.gz
	$(MAKE) vuln description


# The file crypto_sign.tar.gz can be obtained by fetching message #1115
# from the eBATS mailing list archive and following the link therein.
# Concretely, this means sending an email to ebats-get.1115@list.cr.yp.to
# and waiting for the automatic response.
#
# For your convenience, here's the message, omitting some messy headers:
#
# > Message-ID: <891cdfd2-47b4-eaff-11a0-207f3aafa1eb@ntnu.no>
# > Date: Fri, 3 Mar 2023 09:01:58 +0100
# > Subject: SEQUOA signatures inclusion in SUPERCOP and subsequent benchmarking
# > To: ebats@list.cr.yp.to
# > From: Danilo Gligoroski <danilog@ntnu.no>
# >
# > Hi,
# >
# > Please include the following code package of SEQUOA digital signatures
# >
# > https://studntnu-my.sharepoint.com/:u:/g/personal/danilog_ntnu_no/EcKKduF5yEZGkWx6Er8zkugBjksiRyPhMU9DuBZIRurG9w?e=Qas8vW
# >
# > Best regards,
# >
# > Danilo!

crypto_sign.tar.gz:
	@echo -e 'missing $@; read the Makefile for instructions'
	@false


IMPL = crypto_sign/sequoa359classic/ref/

CXXFLAGS += -std=c++17 -fPIC -I . -I $(IMPL)
SRC = vuln.cpp $(IMPL)/sign.cpp $(IMPL)/fips202.c
INC = rng.h
LIB = -lntl

vuln: $(SRC) $(INC)
	$(CXX) $(CXXFLAGS) $(SRC) $(LIB) -o $@

description: $(IMPL)/../description
	ln $< .

rng.h:
	echo '#include <sys/random.h>' >$@
	echo -n 'void randombytes(unsigned char *s, size_t l) { ' >>$@
	echo 'if (l > 256 || -1 == getrandom(s, l, 0)) abort(); }' >>$@

crypto_sign/%: crypto_sign
	@:

crypto_sign: crypto_sign.tar.gz
	echo 3b3e3072834cd3873a5a14134505cfaf66613c9d35e1ccb10c8c1924 $< | sha224sum -c
	tar -xvf $<
	touch $@

.PHONY: clean
clean:
	rm -f vuln rng.h
	rm -f description
	rm -rf crypto_sign/

