import os
import glob

directory = './'
for filename in glob.glob('**/**/**.txt'):
    if filename.endswith('converted.txt'):
        file_path = filename
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(file_path.split('converted.txt')[0]+"headers.txt", 'w', encoding='utf-8') as file:
            for line in lines:
                if line.startswith('$'):
                    line = '<h1>' + line[1:].replace('\n', '') + '</h1>' + '\n'
                elif line.startswith('@'):
                    line = '<h2>' + line[1:].replace('\n', '') + '</h2>' + '\n'
                elif line.startswith('!'):
                    line = '<h3>' + line[1:].replace('\n', '') + '</h3>' + '\n'
                file.write(line)
