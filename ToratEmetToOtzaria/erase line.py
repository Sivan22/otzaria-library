import os
from glob import glob

output_dir = 'output'

for file_path in glob(os.path.join(output_dir, '*')):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.replace('<line>', '').replace('</line>', '')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


