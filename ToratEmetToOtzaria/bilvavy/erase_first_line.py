import os
path = 'bilvavy'
for filename in os.listdir(path):
    if not filename.endswith('converted.txt'):
        continue
    file_path = os.path.join(path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().split('\n', 1)[1]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
