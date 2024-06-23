import re
import os

def manipulate(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read()




        pattern = r"\$(.*?)\n" 
        replacement = r"<h1>\1</h1>\n"  
        lines = re.sub(pattern, replacement, lines)

        pattern = r"#(.*?)\n" 
        replacement = r"<h2>\1</h2>\n"  
        lines = re.sub(pattern, replacement, lines)

        pattern = r"@(.*?)\n" 
        replacement = r"<h3>\1</h3>\n"  
        lines = re.sub(pattern, replacement, lines)

        pattern = r"~(.*?)\n" 
        replacement = r"<h4>\1</h4>\n"  
        lines = re.sub(pattern, replacement, lines)

        pattern = r"\[\[(.*?)\]\]"  
        replacement = r"<b>\1</b>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
        lines= re.sub(pattern, replacement, lines)
        
        pattern = r"<<<<(.*?)>>>>"  # Matches "*any-text*"
        replacement = r"<sup><small>\1</small></sup>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
        lines = re.sub(pattern, replacement, lines)
                    
        pattern = r"<<<(.*?)>>>"  # Matches "*any-text*"
        replacement = r"<small>\1</small>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
        lines = re.sub(pattern, replacement, lines)

        pattern = r"{{{{{(.*?)}}}}}"  # Matches "*any-text*"
        replacement = r"<i>\1</i>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
        lines= re.sub(pattern, replacement, lines)

        pattern = r"{{{{(.*?)}}}}"  # Matches "*any-text*"
        replacement = r"<big>\1</big>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
        lines= re.sub(pattern, replacement, lines)

        pattern = r"{{{(.*?)}}}"  # Matches "*any-text*"
        replacement = r"<big>\1</big>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
        lines= re.sub(pattern, replacement, lines)

        pattern = r"{{(.*?)}}"  # Matches "*any-text*"
        replacement = r"<<div style='border-style:solid; border-width:2; padding:12;'>\1</div>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
        lines= re.sub(pattern, replacement, lines)



        lines = lines.replace('((','<b>').replace('))','</b>')
        lines = lines.replace(r'{{{','<big>').replace(r'}}}','</b>')
        lines = lines.replace(r'{{','').replace(r'}}','')
        lines = lines.replace('<<<','<small>').replace('>>>', '</small>')
        lines = lines.replace('<<<<','<sup><small>').replace('>>>>', '</small></sup>')



        
        with open(path.replace( '.txt', 'manipulated.txt'), 'w', encoding='utf-8') as f:
            f.writelines(lines)

#manipulate('books\\מועדים\\חמדת ימים ומבוא שערי חמדה\\111_chemdat_yamim_1converted.txt')

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
            if file.endswith( 'converted.txt'):
                manipulate(os.path.join(root, file))

process_dir('books\\מועדים\\חמדת ימים ומבוא שערי חמדה')