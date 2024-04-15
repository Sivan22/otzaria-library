import os

output_dir = 'output'

for filename in os.listdir(output_dir):
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith('~'):
                line = line.replace(' - א', '.').replace(' - ב', ':')
            file.write(line)

