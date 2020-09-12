

clean:


all: README.md


README.md: plugin.json
	../community-plugins/generate_plugininfo.py -r
