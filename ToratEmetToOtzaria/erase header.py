import glob

files = glob.glob('output/*')
for file_path in files:
    with open(file_path, 'r',encoding='utf-8') as f:
        content = f.read().split('\n', 1)[1]
    with open(file_path, 'w',encoding='utf-8') as f:
        f.write(content)
