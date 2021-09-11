

clean:
	rm -f *~

all: README.md LICENSE

README.md: plugin.json
	../community-plugins/generate_plugininfo.py -r
LICENSE: plugin.json
	../community-plugins/generate_plugininfo.py -l

install:
	ln -s `pwd` ~/.binaryninja/plugins/symgrate2-binja-plugin || ln -s `pwd` ~/Library/Application\ Support/Binary\ Ninja/plugins/symgrate2-binja-plugin
test:
	python3 test-query.py | grep fopen
	python3 test-binja.py samples/goodmote.bndb | grep NOROM

