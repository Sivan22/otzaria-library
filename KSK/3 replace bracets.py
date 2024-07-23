import os
import re
import glob

def replace_last_reversed(pattern, replacement,text):
  """Replaces the last occurrence of a pattern by reversing the string.

  Args:
    text: The string to modify.
    pattern: The pattern to replace (can use .*? for matching any character).
    replacement: The string to replace the last occurrence with.

  Returns:
    The modified string with the last occurrence replaced.
  """
  reversed_text = text[::-1]
  replacement = replacement[::-1].replace('1\\', '\\1').replace('n\\','\\n')
  new_text = re.sub(pattern, replacement, reversed_text, count=1)
  return new_text[::-1]

directory = './'
for filename in glob.glob('**/**/**.txt'):
    if filename.endswith('headers.txt'):
        file_path = filename
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if "<h3>" in file.read():
                continue
        with open(file_path.replace("headers.txt",'bracets.txt'), 'w', encoding='utf-8') as file:            
            for line in lines:
                reverse_pattern = r"\n\.\](.*?)\[" 
                replacement = r"\n<h3>[\1]</h3>\n" 
                line = replace_last_reversed(reverse_pattern, replacement, line)
                file.write(line)


















