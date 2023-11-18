import argparse
import json
import os

def output(info_list: list, json_path: str, type: str):
    file = dict()

    file[type] = info_list

    dependency_str = json.dumps(file, indent=4)
    with open(json_path, 'w') as json_file:
        json_file.write(dependency_str)

def Dependency(src, dest, kind, project):
    dependency = dict()
    values = dict()

    dependency["src"] = src.replace("\\", '.').replace('..', project)
    dependency["dest"] = dest.replace("\\", '.')
    values["kind"] = kind
    dependency["values"] = values

    return dependency


def pycg(project_name, input_path, output_path):
    with open(input_path, 'r' , encoding='utf8') as json_file:
        data = json.load(json_file)

    dependencyList = list()

    for key, values in data.items():
        for value in values:
            dependencyList.append(Dependency(key, value, "", project_name))

    dependency_json_path = output_path + "pycg_" + project_name + "_dependency.json"
    output(dependencyList, dependency_json_path, "dependency")




parser = argparse.ArgumentParser()
parser.add_argument('lang', help='Sepcify the target language:cpp, java, python, js')
parser.add_argument('project_name', help='Specify the project name')
parser.add_argument('input_path', help='Specify the json path')
parser.add_argument('output_path', help='Specify the output path')
parser.add_argument('prepath', help='Specify the path your project in')
args = parser.parse_args()

project_name = args.project_name
input_path = args.input_path + project_name + '.json'
output_path = args.output_path + project_name + '/'


if not os.path.exists(output_path):
    os.makedirs(output_path)

pycg(project_name, input_path, output_path)
