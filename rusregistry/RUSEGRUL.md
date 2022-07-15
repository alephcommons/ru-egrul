# Russian EGRUL Data to FTM loader

## 1. CSV loader

Usage:
1. Download and unzip all files in https://egrul.itsoft.ru/csv/

to generate links run:
```python3

from rusregistry.csv_processing.utils import get_file_links
links = get_file_links('https://egrul.itsoft.ru/csv/')

with open('CSV_LINKS.txt', 'w') as f:
    f.write(links)

```
(use CSV_LINKS.txt for easy download)

2. Run all cells in `rusregistry/CSV_RUEGRUL.ipynb`
