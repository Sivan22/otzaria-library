import os
import re
import shutil

files = os.listdir('output')

for file in files:
    with open(os.path.join('output', file), 'r+', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'<h1>(.*?)</h1>', content)
        if match:
            name = match.group(1).strip()
            name = name.split('|')[0]
            name = name.replace('-','על')       
            
            shutil.copy(os.path.join('output', file), os.path.join('ביאור חברותא', name )),


