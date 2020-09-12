

clean:
	rm -f *~

all: README.md LICENSE

README.md: plugin.json
	../community-plugins/generate_plugininfo.py -r
LICENSE: plugin.json
	../community-plugins/generate_plugininfo.py -l

install:
	ln -s `pwd` ~/.binaryninja/plugins/symgrate2-binja-plugin
test:
	python3 test-query.py
	python3 test-binja.py

