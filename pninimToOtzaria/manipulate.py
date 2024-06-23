import re
import os

def manipulate(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if(i ==0):
                lines[i] = f'<h1>{line.strip()}</h1>\n'

                
            pattern = r"\%\%\%(.*?)\n" 
            replacement = r"<h6>\1</h6>\n" 
            lines[i] = re.sub(pattern, replacement, lines[i])

            pattern = r"\%\%(.*?)\n" 
            replacement = r"<h5>\1</h5>\n" 
            lines[i] = re.sub(pattern, replacement, lines[i])

            pattern = r"\%(.*?)\n" 
            replacement = r"<h2>\1</h2>\n"  
            lines[i] = re.sub(pattern, replacement, lines[i])

            pattern = r"/(.*?)/" 
            replacement = r"<i>\1</i>"  
            lines[i] = re.sub(pattern, replacement, lines[i])

            pattern = r"\*(.*?)\*"  
            replacement = r"<b>\1</b>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
            lines[i] = re.sub(pattern, replacement, lines[i])
            
            pattern = r"_(.*?)_"  # Matches "*any-text*"
            replacement = r"<u>\1</u>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
            lines[i] = re.sub(pattern, replacement, lines[i])
                        
            pattern = r"\[\^(.*?)\]"  # Matches "*any-text*"
            replacement = r"<sup>\1</sup>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
            lines[i] = re.sub(pattern, replacement, lines[i])

            if (lines[i].startswith('<sup>')):
                lines[i]=f'<small>{lines[i].strip()}</small>\n'

        

        for i, line in enumerate(lines):
            if(line == '\n'):
                lines.remove(line)
            if (i > 0 and re.sub('<[^<]+?>', '', line.replace(' ','')) == re.sub('<[^<]+?>', '', lines[i-1].replace(' ',''))):
                lines.remove(line)


        
        with open(path.replace( 'merged.txt', '.txt'), 'w', encoding='utf-8') as f:
            f.writelines(lines)

manipulate('pninim books\\הלכה\\דרכי_הוראה\\דרכי_הוראהmerged.txt')

def process_dir(path):
    """
    Recursively processes all files in the given directory and its subdirectories.
    
    Args:
        path (str): The path of the directory to be processed.
    
    Returns:
        None
    
    This function uses the os.walk() function to iterate over all files and directories in the given directory and its subdirectories. For each file, it checks if the file ends with 'index'. If it does, it calls the merge_book() function to merge the content of the file with other files in the same directory. The merge_book() function opens the file, reads its content, processes lines that start with '+', and writes the modified content back to the file. The modified content is written to a new file with the same name as the original file, but with the extension changed to '.txt'.
    """
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            process_dir(os.path.join(root,dir))
        for file in files:
            if file.endswith( 'merged.txt'):
                manipulate(os.path.join(root, file))

#process_dir('pninimToOtzaria\pninim books')