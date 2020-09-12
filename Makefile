

clean:
	rm -f *~

all: README.md


README.md: plugin.json
	../community-plugins/generate_plugininfo.py -r

install:
	ln -s `pwd` ~/.binaryninja/plugins/symgrate2-binja-plugin
test:
	python3 test-query.py

