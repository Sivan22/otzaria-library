def find_all_books(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            add_sufffix(os.path.join(root,dir))
        for file in files:
            os.rename(os.path.join(root,file),os.path.join(root,file).split('.')[0]+'.txt')