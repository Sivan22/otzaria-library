import re
import os

def manipulate(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
           
            pattern = r"\[\^(.*?)\]"  # Matches "*any-text*"
            replacement = r"<sup>\1</sup>"  # Replaces with "<b>\1</b>" (where \1 is captured text)
            lines[i] = re.sub(pattern, replacement, lines[i])

            if (lines[i].startswith('<sup>')):
                lines[i]=f'<small>{lines[i].strip()}</small>\n'
        
        with open(path+'.txt', 'w', encoding='utf-8') as f:
            f.writelines(lines)

manipulate('תורת_נביאים.txt')
