import json
import sys
import csv
import requests
import os, glob

if __name__ == '__main__':
    project_path_list = ["..\Data\RQ2\micro-benchmark B\Benchmark-collectedbyPyCG\args\assigned_call"]  #You should modify the paths within this list to the paths of the projects you intend to analyze.
    for index_path, project_path in enumerate(project_path_list):
        print(project_path)
        project_file_list = [f for f in glob.glob(f'{project_path}/**/*.py', recursive=True)]
        project_name = project_path.split("\\")[-1]
        current_dir = os.path.dirname(__file__)
        save_parent_path = os.path.join(current_dir, project_name)

        for index, fp in enumerate(project_file_list):
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    r = requests.post("http://localhost:5001/api/predict?tc=0", f.read())
                    dirname, filename = os.path.split(fp)
                    if len(dirname.split(project_name + "\\")) == 1:
                        save_path_dir = save_parent_path
                    else:
                        save_children_dir = dirname.split(project_name + "\\")[-1]
                        save_path_dir = os.path.join(save_parent_path, save_children_dir)
                    if not os.path.exists(save_path_dir):
                        os.makedirs(save_path_dir)
                    save_file_name = filename.split(".")[0] + ".json"
                    with open(save_path_dir + "\\" + save_file_name, "w") as f1:
                        f1.write(json.dumps((r.json())))
                except Exception as e:
                    print("error")
                    with open("errors.log", "a") as f2:
                        f2.write(fp)
                        f2.write(str(e))
                        continue
