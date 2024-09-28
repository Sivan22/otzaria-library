import csv
import json

list_all = ['underwentBerelUnflagging', 'categoryEnglish', 'printYear', 'ocrFeDir',
             'printLocationEnglish', 'textFileURL', 'notHumanReviewed', 'category',
             'source', 'author', 'printLocation', 'displayName', 'nikudMetegFileURL',
               'OCRDataURL', 'authorEnglish', 'fileName', 'displayNameEnglish']

with open("new_books.json", "r", encoding="utf-8") as json_file:
    json_content = json.load(json_file)
with open("csv.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(list_all)
    for i in json_content:
        new_dict = {}
        for item in list_all:
            new_dict[item] = i.get(item) if i.get(item) else ""
        writer.writerow(list(new_dict.values()))