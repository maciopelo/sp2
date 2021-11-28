import os

def flatten(l):
    return [item for sublist in l for item in sublist]

def add_path(path, files):
    return [path + file for file in files]

root = './tests/'
folders = os.listdir(root)
files = flatten([add_path(root + folder + '/', os.listdir(root + folder)) for folder in folders])

for file_path in files:
    with open(file_path, 'r+') as f:
        contents = f.read()
        if 'check' in contents or 'group' in contents:
            print(file_path)
            f.seek(0)
            f.write(contents.replace('check', 'if').replace('group', 'list'))
            f.truncate()