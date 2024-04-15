
import os
import shutil

source_dir = '.'
output_dir = 'output'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file == 'HavTempNoNotes.txt':
            filename = os.path.join(root, file)
            dst = os.path.join(output_dir, os.path.relpath(root, source_dir).replace(os.path.sep, '_') + '_' + file)
            shutil.copy(filename, dst)

