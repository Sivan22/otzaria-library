import os

file_path = '106_1_KITZUR_YALKUT_YOSEF.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
with open('קיצור ילקוט יוסף.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        if line.startswith('$'):
            line = '<h1>' + line[1:].replace('\n', '') + '</h1>' + '\n'
        elif line.startswith('#'):
            line = '<h2>' + line[1:].replace('\n', '') + '</h2>' + '\n'
        elif line.startswith('@'):
            line = '<h3>' + line[1:].replace('\n', '') + '</h3>' + '\n'
        elif line.startswith('~'):
            line = '<h4>' + line[1:].replace('\n', '') + '</h4>' + '\n'
        elif line.startswith('!'):
            line = '(' + (line[1:].replace('\n', '').replace(' ', '')) + ')'+ ' '
        file.write(line)
