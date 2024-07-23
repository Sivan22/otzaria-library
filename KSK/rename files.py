import os
import glob

directory = './'
for filename in glob.glob('**/**/**.txt'):
    if filename.endswith('bracets.txt'):
        file_path = filename
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines = lines[2:]
        while lines[0].strip() == '': lines = lines[1:] 
        book_name = "קובץ שיטות קמאי על"+lines[0].strip().replace('מסכת',"")       
        with open(os.path.join (os.path.dirname(filename),book_name+'.txt'), 'w', encoding='utf-8') as file:
            lines[0] = f'<h1>{book_name}</h1>\n'
            #remove empty lines
            for line in lines:
                if line.strip() == '': lines.remove(line)            
            file.writelines(lines)
