
build: data/export/egrul.json

data/export/egrul.json: data/sorted.json
	mkdir -p data/export
	ftm sorted-aggregate -i data/sorted.json -o data/export/egrul.json

data/sorted.json: data/fragments.json
	sort -S 2G -o data/sorted.json data/fragments.json

data/fragments.json:
	python parse_xml.py
