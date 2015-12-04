package: metadata.txt __init__.py algo.svg micro.svg
	rm -rf qgis_microprocessing
	mkdir qgis_microprocessing
	cp $^ qgis_microprocessing/
	rm -f qgis_microprocessing.zip
	zip  -r qgis_microprocessing.zip qgis_microprocessing
	rm -r qgis_microprocessing

install: package
	rm -rf ${HOME}/.qgis2/python/plugins/qgis_microprocessing
	unzip -o qgis_microprocessing.zip -d ${HOME}/.qgis2/python/plugins
	rm -f qgis_microprocessing.zip


