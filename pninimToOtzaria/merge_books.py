import os


def merge_book(book_name):
    """
    Opens a book file, reads its content, processes lines that start with '+', and writes the modified content back to the file.
    :param book_name: The path of the book file to be processed.
    """
    with open(book_name, 'r', encoding='utf-8') as index_file:
        text = index_file.readlines()
    for line in text:
        if line.startswith('+'):            
            try :
                with open(book_name.replace('\\index','')+'\\'+ line[2:-2], 'r', encoding='utf-8') as f:
                    text += f.readlines()
            except:
                print(line)
            text.remove(line)    
    with open(book_name.replace('index','')+ '\\' + book_name.split('\\')[-2] + '.txt', 'w', encoding='utf-8') as f:
        f.writelines(text)



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
            if file.endswith('index'):
                merge_book(os.path.join(root, file))

process_dir('pninimToOtzaria\pninim books')
