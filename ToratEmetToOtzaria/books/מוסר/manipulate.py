
with open('מנורת המאור מוסר\\300_menorat_hamaorconverted.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
with open('menorat', 'w', encoding='utf-8') as new_file:
    for line in lines:
        if line.startswith('$') :
            line = '<h1>' + line[1:].replace('\n', '') + '</h1>' + '\n'
        elif line.startswith('^') or line.startswith('#'):
            line = '<h2>' + line[1:].replace('\n', '') + '</h2>' + '\n'
        elif line.startswith('#'):
            line = '<h3>' + line[1:].replace('\n', '') + '</h3>' + '\n'
        elif line.startswith('@'):
            line = '<h4>' + line[1:].replace('\n', '') + '</h4>' + '\n'
        elif line.startswith('~'):
            line = '<h5>' + line[1:].replace('\n', '') + '</h5>' + '\n'

        new_file.write(line)
