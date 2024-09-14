import xml.etree.ElementTree as ET
import json


def process_node(node, dic_all):
    # Get the name attribute from the node
    node_name = node.get("name")
    if "nid" in node.attrib:
        nid = node.get("nid")
        if dic_all.get(nid):
            dic_all[nid] += [node_name]
        else:
            dic_all[nid] = [node_name]
    if node.findall("node"):
        # Recursively process child nodes within the created folder
        for child_node in node.findall("node"):
            process_node(child_node, dic_all)
    return dic_all

xml_file = r"fix_tnc.xml"
tree = ET.parse(xml_file)
root = tree.getroot()
dic_all = {}
dic = process_node(root, dic_all)
print(dic)
with open("duble.json", "w", encoding = "utf-8") as file:
    json.dump(dic, file, ensure_ascii=False, indent=4)