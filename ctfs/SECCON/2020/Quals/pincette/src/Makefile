PIN_ROOT=/opt/pin
TOPTARGETS := all clean
SUBDIRS := pintool

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

install:
	install -m 755 -d /opt/pincette
	install -m 644 -t /opt/pincette\
		server/flag
	install -m 755 -t /opt/pincette\
		pintool/obj-intel64/ibt.so\
		server/server.py\
		server/vuln
	install -m 755 -d /etc/xinetd.d
	install -m 644 -t /etc/xinetd.d\
                server/pincette_server_conf

.PHONY: $(TOPTARGETS) $(SUBDIRS) install

