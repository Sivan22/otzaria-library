import os
file_name = 'bilvavy\\073_bilvavi3.txt'
with open(file_name, 'r', encoding='utf-8') as file:
    lines = file.readlines()
with open(file_name.split('.')[0]+'converted.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        if line.startswith('$') :
            line = '<h1>' + line[1:].replace('\n', '') + '</h1>' + '\n'
        elif line.startswith('#'):
            line = '<h2>' + line[1:].replace('\n', '') + '</h2>' + '\n'
        elif line.startswith('@'):
            line = '<h3>' + line[1:].replace('\n', '') + '</h3>' + '\n'
        elif line.startswith('~'):
            line = '<h4>' + line[1:].replace('\n', '') + '</h4>' + '\n'
        new_file.write(line)
