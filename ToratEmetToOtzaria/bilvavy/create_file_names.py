import os

path = 'bilvavy'
for file_name in os.listdir(path):
    with open(os.path.join(path, file_name), 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith('<h1>'):
            new_file_name = line[4:-6] + '.txt'
            os.rename(os.path.join(path, file_name), os.path.join(path, new_file_name))
            break

