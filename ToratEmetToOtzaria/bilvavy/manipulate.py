import os
path = 'bilvavy'
for file_name in os.listdir(path):
    with open(os.path.join(path, file_name), 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open((os.path.join(path, file_name).split('.')[0])+'converted.txt', 'w', encoding='utf-8') as new_file:
        for line in lines:
            if line.startswith('$') :
                line = '<h1>' + line[1:].replace('\n', '') + '</h1>' + '\n'
            elif line.startswith('@') or line.startswith('#'):
                line = '<h2>' + line[1:].replace('\n', '') + '</h2>' + '\n'
            elif line.startswith('~'):
                line = '<h3>' + line[1:].replace('\n', '') + '</h3>' + '\n'
            new_file.write(line)
