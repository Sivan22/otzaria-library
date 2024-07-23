import glob
from charset_normalizer import from_path
import os
from pathlib import Path


path = './'
for filename in glob.glob('**/**/**.txt'):
    if not filename.endswith('.txt'):
        continue
    file_path = filename
    print("Converting " + filename)

    with open(file_path, 'r', encoding='ansi') as f:
            content = f.read()
    with open(file_path.split('.txt')[0]+'converted.txt', 'w', encoding='UTF-8') as f:
            f.write(content)
    print("Converted " + filename)