import json

def addLink(menorat:list, nefesh:list ):
    with open('links.json','a') as file:
        file.write(json.dump({'index_1':menorat.__len__(),'index_2':nefesh.__len__(),'path_2':'מנורת המאור (אבוהב)','heRef':'נפש יהודה'}))


with open('מנורת המאור מוסר\\300_menorat_hamaorconverted.txt') as 