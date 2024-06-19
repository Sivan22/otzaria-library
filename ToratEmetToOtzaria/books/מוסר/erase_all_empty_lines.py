import os
path = 'bilvavy'
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip():
                file.write(line)
