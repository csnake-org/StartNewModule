import os.path

def getRootFolder():
    root = os.path.dirname(__file__) + "/../"
    root = os.path.normpath(root).replace("\\", "/")
    return root
