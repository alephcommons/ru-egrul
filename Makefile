
build: data/export/egrul.json

publish: data/export/egrul.json
	aws s3 sync --no-progress --cache-control "public, max-age=64600" --metadata-directive REPLACE --acl public-read data/export s3://data.opensanctions.org/contrib/ru_egrul

data/export/egrul.json: data/sorted.json
	mkdir -p data/export
	ftm sorted-aggregate -i data/sorted.json -o data/export/egrul.json

data/sorted.json: data/fragments.json
	sort -S 2G -o data/sorted.json data/fragments.json

data/fragments.json:
	python parse_xml.py

