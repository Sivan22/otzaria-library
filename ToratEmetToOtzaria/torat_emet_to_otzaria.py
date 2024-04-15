import glob


def convert_to_utf8(dir_path):
    file_list = glob.glob(dir_path, recursive=True)
    for filename in file_list:
        with open(filename, 'r', encoding='ANSI') as f:
            content = f.read()
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(content)
        print("Converted " + filename)

convert_to_utf8(r'C:\\dev\\otzaria_library\\ToratEmetToOtzaria\\**\\**\\**\\**\\**.txt')

