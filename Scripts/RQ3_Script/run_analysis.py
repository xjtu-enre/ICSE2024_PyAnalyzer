import json
import os

import shutil
def move_file(source, destination):
    try:
        shutil.move(source, destination)
    except FileNotFoundError:
        print("error")
    except PermissionError:
        print("no permission")

with open('data/project.json') as f:
    data = json.load(f)
for item in data:
    proj = next(iter(item))

    os.system("python Pyre.py "+ proj)
    os.system("python analysis.py " + proj)
    source_file = 'result/'+proj+'/gt/'+proj+'_acc.csv'
    destination_dir = 'result/acc/'
    if os.path.exists(destination_dir+proj+'_acc.csv'):
        os.remove(destination_dir+proj+'_acc.csv')
    move_file(source_file,destination_dir)