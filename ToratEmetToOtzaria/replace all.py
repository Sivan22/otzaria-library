import os

path = 'output'

for filename in os.listdir(path):
    if not filename.endswith('.txt'):
        continue
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            line = line.replace('(((', '<big><b>')
            line = line.replace(')))', '</b></big>')
            line = line.replace('{', '<b>')
            line = line.replace('}', '</b>')
            if line.strip() == '':
                continue
            file.write(line)

