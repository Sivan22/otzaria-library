
import os

path = 'output'
for filename in os.listdir(path):
    if not filename.endswith('.txt'):
        continue
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='ANSI') as f:
        content = f.read()
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(content)
    print("Converted " + filename)





















