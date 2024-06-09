
import glob
from charset_normalizer import from_path
import os
from pathlib import Path


path = 'books'
for filename in glob.glob(path + '/*/*.txt'):
    if not filename.endswith('.txt'):
        continue
    file_path = filename
    print("Converting " + filename)

    with open(file_path, 'r', encoding='cp1255') as f:
            content = f.read()
    output_file = Path('output'+file_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open('output'+file_path, 'w', encoding='UTF-8') as f:
            f.write(content)
    print("Converted " + filename)





















