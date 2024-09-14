import os
import xml.etree.ElementTree as ET
import re
import shutil

 
def sanitize_filename(name):
    # Remove problematic characters from the filename
    return re.sub(r'[\\/*?:"<>|]', '', name).strip()
 
def process_node(node, base_folder=""):
    # Get the name attribute from the node
    node_name = node.get("name")
 
    # Check if the node has a nid attribute
    if "nid" in node.attrib:
        nid = node.get("nid")
        # Sanitize the filename and rename the file
        new_filename = os.path.join(base_folder, sanitize_filename(node_name) + ".txt")
        old_filename = os.path.join(book_folder, nid + ".xml")
        if os.path.exists(old_filename):
            print(new_filename)
            os.makedirs(os.path.dirname(new_filename), exist_ok=True)
            shutil.copy(old_filename, new_filename)
            #print(f"Moved and renamed file: {old_filename} to {new_filename}")
        else:
        	print(nid)
 
    # Check if the node has child nodes
    if node.findall("node"):
        folder_name = os.path.join(base_folder,sanitize_filename(node_name))
 
        # Recursively process child nodes within the created folder
        for child_node in node.findall("node"):
            process_node(child_node, folder_name)
 
# Parse the XML file
xml_file = r"fix_tnc.xml"
tree = ET.parse(xml_file)
book_folder = "xml"
root = tree.getroot()
# Process the root node
process_node(root)