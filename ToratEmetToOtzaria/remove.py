import os

for file in os.listdir('output'):
    if not file.endswith('.txt'):
        continue
    with open(os.path.join('output', file), 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('| בלי הערות', '', 1)
    with open(os.path.join('output', file), 'w', encoding='utf-8') as f:
        f.write(content)
