import os
import re
import shutil

files = os.listdir('./')

for file in files: 
    if file.endswith('.pdf'):
        shutil.copy(os.path.join('./', file), os.path.join('output', file.split('.')[0]+'צורת הדף.pdf')),


