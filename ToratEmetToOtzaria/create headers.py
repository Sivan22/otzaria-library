import os

directory = 'output'
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if line.startswith('$'):
                    line = '<h1>' + line[1:].replace('\n', '') + '</h1>' + '\n'
                elif line.startswith('^'):
                    line = '<h2>' + line[1:].replace('\n', '') + '</h2>' + '\n'
                elif line.startswith('~'):
                    line = '<h3>' + line[1:].replace('\n', '') + '</h3>' + '\n'
                file.write(line)
