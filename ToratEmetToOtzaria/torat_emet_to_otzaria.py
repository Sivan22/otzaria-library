import os
import chardet

toratEmetDirectory = <path to torat emet directory>
outputDirectory = "ToratEmetoutput"



#check encoding of files in toratEmetDirectory and convert if not utf-8
def convert_encoding(dir):
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            convert_encoding(os.path.join(root, dir))
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
            if result['encoding'] != 'utf-8':
                with open(file_path, 'rb') as f:
                    content = f.read().decode(result['encoding'])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            print(file_path)

convert_encoding(toratEmetDirectory)



