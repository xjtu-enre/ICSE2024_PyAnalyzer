
import argparse
import json
import os

import pandas as pd

df = pd.DataFrame()

parser = argparse.ArgumentParser()
parser.add_argument('project')
args = parser.parse_args()
project_name = args.project

input_path = "result/" + project_name
output_path = "result/" + project_name + "/gt/"

gt_path = output_path + 'gt_dependency.json'
filtered_gt_path = output_path + 'filtered_gt_dependency.json'

with open(gt_path, 'r', encoding='utf-8') as gt_file:
    gt = json.load(gt_file)['dependency']
with open(filtered_gt_path, 'r', encoding='utf-8') as filtered_file:
    filtered_gt = json.load(filtered_file)['dependency']


def filters(project_name, tool, data):
    datalist = list()
    data_filtered_list = list()
    with open("data/rr.json", 'r', encoding='utf8') as filter_items:
        try:
            filters = json.load(filter_items)[project_name]
        except:
            filters = []
    extra = set()
    for item in data:
        if type(item['src']) == int or type(item['dest']) == int:
            continue

        datalist.append(item)

        if item['src'].startswith(tuple(filters)) and \
                item['dest'].startswith(tuple(filters)) and len(filters) != 0:
            data_filtered_list.append(item)
        else:
            if item['src'].startswith(tuple(filters)):
                extra.add(item['dest'])
            else:
                extra.add(item['src'])

    output_path = "result/" + project_name + '/extra/'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(output_path + tool + '.json', 'w') as result:
        result.write(str(list(extra)))

    return datalist, data_filtered_list


def match_mod1(gt, dependency):
    flex_num = 0
    strict_num = 0

    for item1 in gt:
        flag1 = False
        flag2 = False

        for item2 in dependency:

            if (item2['src'].endswith(item1['src']) and item2['dest'].endswith(item1['dest'])) or \
                    (item1['src'].endswith(item2['src']) and item1['dest'].endswith(item2['dest'])):
                flag1 = True
                if item1['location']['startLine'] == item2['location']['startLine'] and \
                        item1['location']['startCol'] == item2['location']['startCol']:
                    flag2 = True
                    break

        if flag1: flex_num += 1
        if flag2: strict_num += 1

    return flex_num, strict_num


def match_mod2(gt, dependency):
    flex_num = 0
    strict_num = 0
    flex = list()
    strict = list()
    for item1 in gt:
        flag1 = False
        flag2 = False

        for item2 in dependency:

            if (item2['file'].endswith(item1['location']['path']) and
                item2['dest'].endswith(item1['dest'])) or \
                    (item1['location']['path'].endswith(item2['file']) and
                     item1['dest'].endwith(item2['dest'])):
                # flex_num += 1
                flag1 = True
                flex_dict = dict()
                flex_dict['gt_src'] = item1['src']
                flex_dict['und_src'] = item2['src']
                flex_dict['gt_dest'] = item1['dest']
                flex_dict['und_dest'] = item2['dest']
                flex.append(flex_dict)
                if item1['location']['startLine'] == item2['location']['startLine'] and \
                        item1['location']['startCol'] == item2['location']['startCol']:
                    # strict_num += 1
                    flag2 = True
                    break
        if flag1: flex_num += 1
        if flag2: strict_num += 1
    return flex_num, strict_num


def match_mod3(gt, dependency):
    flex_num = 0
    strict_num = 0
    flex = list()
    strict = list()
    for item1 in gt:
        flag1 = False
        flag2 = False
        for item2 in dependency:

            if item1['src'].split('.')[-1] == item2['src'].split('.')[-1] \
                    and item1['dest'].split('.')[-1] == item2['dest'].split('.')[-1]:
                flag1 = True
                flex_dict = dict()
                flex_dict['gt_src'] = item1['src']
                flex_dict['depends_src'] = item2['src']
                flex_dict['gt_dest'] = item1['dest']
                flex_dict['depends_dest'] = item2['dest']
                flex.append(flex_dict)
                if item1['location']['startLine'] == item2['location']['startLine'] and \
                        item1['location']['startCol'] == item2['location']['startCol']:
                    flag2 = True
        if flag1: flex_num += 1
        if flag2: strict_num += 1

    return flex_num, strict_num


def match_mod4(gt, dependency):
    flex_num = 0
    strict_num = 0
    flex = list()
    strict = list()
    for item1 in gt:
        for item2 in dependency:
            if (item2['src'].endswith(item1['src']) and item2['dest'].endswith(item1['dest'])) or \
                    (item1['src'].endswith(item2['src']) and item1['dest'].endswith(item2['dest'])):
                flex_num += 1

                flex_dict = dict()
                flex_dict['gt_src'] = item1['src']
                flex_dict['pycg_src'] = item2['src']
                flex_dict['gt_dest'] = item1['dest']
                flex_dict['pycg_dest'] = item2['dest']
                flex.append(flex_dict)
                break

    return flex_num, strict_num

def analyse_und(project_name, input_path, output_path):
    filter = "D:/Programs/SciTools/conf/understand/python/python3/"
    dependency_path = input_path + '/Understand_' + project_name + '_dependency.json'
    entity_path = input_path + '/Understand_' + project_name + '_entity.json'

    with open(dependency_path, 'r', encoding='utf8') as json_file:
        dependency = json.load(json_file)['dependency']

    with open(entity_path, 'r', encoding='utf8') as entity_file:
        entity = json.load(entity_file)['entity']

    entity_dict = {}
    for item in entity:
        if item['qualifiedName'].endswith('.py'):
            item['qualifiedName'] = item['qualifiedName'][:-3]
        item['qualifiedName'] = item['qualifiedName'].replace(filter, '').replace('/', '.')
        while item['qualifiedName'].startswith('.'):
            item['qualifiedName'] = item['qualifiedName'][1:]
        entity_dict[item['id']] = item

    for item in dependency:
        if item['src'] in entity_dict and item['dest'] in entity_dict:
            item['src'] = entity_dict[item['src']]['qualifiedName']
            item['dest'] = entity_dict[item['dest']]['qualifiedName']

    dependency, filtered_dependency = filters(project_name, 'und', dependency)

    flex_num, strict_num = match_mod1(gt, dependency)
    f_flex_num, f_strict_num = match_mod1(filtered_gt, filtered_dependency)



    acc_path = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc_path)
    data['understand_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)

    data['understand_acc'] = ["{:.2f}".format(flex_num / len_gt),
                              "{:.2f}".format(strict_num / len_gt),
                              "{:.2f}".format(f_flex_num / len_filtered_gt),
                              "{:.2f}".format(f_strict_num / len_filtered_gt)]

    data.to_csv(acc_path)
    outfile = output_path + 'understand_temp.json'
    # json.dumps(dependency, indent=4)
    dependency_str = json.dumps(dependency, indent=4)
    with open(outfile, 'w') as json_file:
        json_file.write(dependency_str)


def analyse_srctrl(project_name, input_path, output_path):
    filter = "D:/Programs/SciTools/conf/understand/python/python3/"
    dependency_path = input_path + '/sourcetrail_' + project_name + '_dependency.json'
    entity_path = input_path + '/sourcetrail_' + project_name + '_entity.json'

    with open(dependency_path, 'r', encoding='utf8') as json_file:
        dependency = json.load(json_file)['relations']

    with open(entity_path, 'r', encoding='utf8') as entity_file:
        entity = json.load(entity_file)['entities']

    entity_dict = {}
    for item in entity:
        if item['qualifiedName'].endswith('.py'):
            item['qualifiedName'] = item['qualifiedName'][:-3]
        item['qualifiedName'] = item['qualifiedName'].replace(filter, '').replace('/', '.')
        while item['qualifiedName'].startswith('.'):
            item['qualifiedName'] = item['qualifiedName'][1:]
        entity_dict[item['id']] = item

    for item in dependency:
        if item['src'] in entity_dict and item['dest'] in entity_dict:
            item['src'] = entity_dict[item['src']]['qualifiedName']
            item['dest'] = entity_dict[item['dest']]['qualifiedName']

    dependency, filtered_dependency = filters(project_name, 'srctrl', dependency)

    flex_num, strict_num = match_mod1(gt, dependency)
    f_flex_num, f_strict_num = match_mod1(filtered_gt, filtered_dependency)

    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)

    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['srctrl_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['srctrl_acc'] = ["{:.2f}".format(flex_num / len_gt),
                          "{:.2f}".format(strict_num / len_gt),
                          "{:.2f}".format(f_flex_num / len_filtered_gt),
                          "{:.2f}".format(f_strict_num / len_filtered_gt)]
    data.to_csv(acc, index=False)


def analyse_pysonar(project_name, input_path, output_path):
    dependency_path = input_path + '/PySonar2_' + project_name + '_dependency.json'
    entity_path = input_path + '/PySonar2_' + project_name + '_entity.json'

    with open(dependency_path, 'r', encoding='utf8') as json_file:
        dependency = json.load(json_file)['dependency']

    for item in dependency:
        if item['dest'].endswith('.py'):
            item['dest'] = item['dest'][:-3]
        item['dest'] = item['dest'].replace('/', '.')
        while item['dest'].startswith('.'):
            item['dest'] = item['dest'][1:]
        item['src'] = item['dest']

    dependency, filtered_dependency = filters(project_name, 'pysonar', dependency)

    flex_num, strict_num = match_mod2(gt, dependency)
    f_flex_num, f_strict_num = match_mod2(filtered_gt, filtered_dependency)
    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['pysonar2_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['pysonar2_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                            "{:.2f}".format(f_flex_num / len_filtered_gt),
                            "{:.2f}".format(f_strict_num / len_filtered_gt)]
    data.to_csv(acc, index=False)



def analyse_depends(project_name, input_path, output_path):
    filter = "D:/Programs/SciTools/conf/understand/python/python3/"
    dependency_path = input_path + '/depends_' + project_name + '_dependency.json'
    entity_path = input_path + '/depends_' + project_name + '_entity.json'

    # detail_path = input_path + project_name + '.txt'
    with open(dependency_path, 'r', encoding='utf8') as json_file:
        dependency = json.load(json_file)['dependency']

    with open(entity_path, 'r', encoding='utf8') as entity_file:
        entity = json.load(entity_file)['entity']

    entity_dict = {}

    for item in entity:
        if item['qualifiedName'].endswith('.py'):
            item['qualifiedName'] = item['qualifiedName'][:-3]
        item['qualifiedName'] = item['qualifiedName'].replace(filter, '').replace('/', '.')
        while item['qualifiedName'].startswith('.'):
            item['qualifiedName'] = item['qualifiedName'][1:]
        entity_dict[item['id']] = item

    for item in dependency:
        if item['src'] in entity_dict and item['dest'] in entity_dict:
            item['src'] = entity_dict[item['src']]['qualifiedName']
            item['dest'] = entity_dict[item['dest']]['qualifiedName']

    dependency, filtered_dependency = filters(project_name, 'depends', dependency)


    flex_num, strict_num = match_mod3(gt, dependency)
    f_flex_num, f_strict_num = match_mod3(filtered_gt, filtered_dependency)

    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['depends_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['depends_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                           "{:.2f}".format(f_flex_num / len_filtered_gt),
                           "{:.2f}".format(f_strict_num / len_filtered_gt)]
    data.to_csv(acc, index=False)



def analyse_pycg(project_name, input_path, output_path):
    filter = "D:/Programs/SciTools/conf/understand/python/python3/"
    dependency_path = input_path + '/pycg_' + project_name + '_dependency.json'

    # detail_path = input_path + project_name + '.txt'
    with open(dependency_path, 'r', encoding='utf8') as json_file:
        dependency = json.load(json_file)['dependency']

    for item in dependency:
        item['src'] = item['src'].replace('\\', '.').replace('<', '.')
        item['dest'] = item['dest'].replace('\\', '.').replace('<', '.')
        while item['src'].startswith('.'):
            item['src'] = item['src'][1:]
        while item['dest'].startswith('.'):
            item['dest'] = item['dest'][1:]

    dependency, filtered_dependency = filters(project_name, 'pycg', dependency)


    flex_num, strict_num = match_mod4(gt, dependency)
    f_flex_num, f_strict_num = match_mod4(filtered_gt, filtered_dependency)
    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['pycg_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['pycg_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                        "{:.2f}".format(f_flex_num / len_filtered_gt),
                        "{:.2f}".format(f_strict_num / len_filtered_gt)]
    data.to_csv(acc, index=False)


def analyse_pyanalyzer(project_name, input_path, output_path):
    filter = "D:/Programs/SciTools/conf/understand/python/python3/"
    json_path = input_path + '-report-pyanalyzer.json'

    # detail_path = input_path + project_name + '.txt'
    with open(json_path, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)

    entity = data['variables']
    dependency = data['cells']

    entity_dict = {}
    for item in entity:
        if item['qualifiedName'].endswith('.py'):
            item['qualifiedName'] = item['qualifiedName'][:-3].replace(filter, '').replace('/', '.')
        entity_dict[item['id']] = item

    for item in dependency:
        if item['src'] in entity_dict and item['dest'] in entity_dict:
            item['src'] = entity_dict[item['src']]['qualifiedName']
            item['dest'] = entity_dict[item['dest']]['qualifiedName']

    dependency, filtered_dependency = filters(project_name, 'pyanalyzer', dependency)

    flex_num, strict_num = match_mod1(gt, dependency)
    f_flex_num, f_strict_num = match_mod1(filtered_gt, filtered_dependency)

    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['pyanalyzer_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['pyanalyzer_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                        "{:.2f}".format(f_flex_num / len_filtered_gt),
                        "{:.2f}".format(f_strict_num / len_filtered_gt)]
    data.to_csv(acc, index=False)



def analyse_enre19(project_name, input_path, output_path):
    filter = "D:/Programs/SciTools/conf/understand/python/python3/"
    json_path = input_path + '_allExpImp_call.json'

    # detail_path = input_path + project_name + '.txt'
    with open(json_path, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)

    entity = data['variables']
    dependency = data['cells']

    for item in dependency:
        item['src'] = entity[item['src']]
        item['dest'] = entity[item['dest']]

    dependency, filtered_dependency = filters(project_name, 'enre19', dependency)

    flex_num, strict_num = match_mod4(gt, dependency)
    f_flex_num, f_strict_num = match_mod4(filtered_gt, filtered_dependency)
    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['enre19_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['enre19_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                           "{:.2f}".format(f_flex_num / len_filtered_gt),
                           "{:.2f}".format(f_strict_num / len_filtered_gt)]
    data.to_csv(acc, index=False)



def analyse_pyanalyzercfg(project_name, input_path, output_path):
    filter = "D:/Programs/SciTools/conf/understand/python/python3/"
    json_path = input_path + '-report-pyanalyzer.json'

    with open(json_path, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)

    entity = data['variables']
    dependency = data['cells']

    entity_dict = {}
    for item in entity:
        if item['qualifiedName'].endswith('.py'):
            item['qualifiedName'] = item['qualifiedName'][:-3]
        item['qualifiedName'] = item['qualifiedName'].replace(filter, '').replace('/', '.')
        entity_dict[item['id']] = item

    for item in dependency:
        if item['src'] in entity_dict and item['dest'] in entity_dict:
            item['src'] = entity_dict[item['src']]['qualifiedName']
            item['dest'] = entity_dict[item['dest']]['qualifiedName']

    dependency, filtered_dependency = filters(project_name, 'pyanalyzercfg', dependency)

    flex_num, strict_num = match_mod1(gt, dependency)
    f_flex_num, f_strict_num = match_mod1(filtered_gt, filtered_dependency)

    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['pyanalyzercfg_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['pyanalyzercfg_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                           "{:.2f}".format(f_flex_num / len_filtered_gt),
                           "{:.2f}".format(f_strict_num / len_filtered_gt)]

    data.to_csv(acc, index=False)


def analyse_callgraph(project_name, input_path, output_path):
    dependency_path = input_path + '/cfg-callgraph-' + project_name + '-dependency.json'

    with open(gt_path, 'r', encoding='utf-8') as gt_file:
        gt = json.load(gt_file)['dependency']
    with open(filtered_gt_path, 'r', encoding='utf-8') as filtered_file:
        filtered_gt = json.load(filtered_file)['dependency']

    with open(dependency_path, 'r', encoding='utf8') as json_file:
        dependency = json.load(json_file)['dependency']

    for item in dependency:
        item['src'] = item['src'].replace('\\', '.').replace('<', '.')
        item['dest'] = item['dest'].replace('\\', '.').replace('<', '.')
        while item['src'].startswith('.'):
            item['src'] = item['src'][1:]
        while item['dest'].startswith('.'):
            item['dest'] = item['dest'][1:]

    dependency, filtered_dependency = filters(project_name, 'pycg', dependency)
    flex_num, strict_num = match_mod4(gt, dependency)
    f_flex_num, f_strict_num = match_mod4(filtered_gt, filtered_dependency)
    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['callgraph_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['callgraph_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                             "{:.2f}".format(f_flex_num / len_filtered_gt),
                             "{:.2f}".format(f_strict_num / len_filtered_gt)]

    data.to_csv(acc, index=False)


def analyse_type4py(project_name, input_path, output_path):
    dependency_path = input_path + "gt_dependency.json"
    filtered_path = input_path + "filtered_gt_dependency.json"

    with open(gt_path, 'r', encoding='utf-8') as gt_file:
        gt = json.load(gt_file)['dependency']
    with open(filtered_gt_path, 'r', encoding='utf-8') as filtered_file:
        filtered_gt = json.load(filtered_file)['dependency']

    with open(dependency_path, 'r', encoding='utf8') as json_file:
        dependency = json.load(json_file)['dependency']

    with open(filtered_path, 'r', encoding='utf8') as json_file:
        filtered_dependency = json.load(json_file)['dependency']

    flex_num, strict_num = match_mod1(gt, dependency)
    f_flex_num, f_strict_num = match_mod1(filtered_gt, filtered_dependency)

    acc = output_path + project_name + '_acc.csv'
    data = pd.read_csv(acc)
    len_gt = max(len(gt), 1)
    len_filtered_gt = max(len(filtered_gt), 1)
    data['type4py_num'] = [flex_num, strict_num, f_flex_num, f_strict_num]
    data['type4py_acc'] = ["{:.2f}".format(flex_num / len_gt), "{:.2f}".format(strict_num / len_gt),
                           "{:.2f}".format(f_flex_num / len_filtered_gt),
                           "{:.2f}".format(f_strict_num / len_filtered_gt)]

    data['gt'] = [len(gt), len(gt), len(filtered_gt), len(filtered_gt)]
    data.to_csv(acc, index=False)


data = {
    project_name: ['flexible', 'strict', 'filtered_flexible', 'filtered_strict'],
}
df_acc = pd.DataFrame(data)
acc = output_path + project_name + '_acc.csv'

df_acc.to_csv(acc, index=False, header=True)

analyse_und(project_name, input_path, output_path)
analyse_srctrl(project_name, input_path, output_path)
analyse_pysonar(project_name, input_path, output_path)
analyse_depends(project_name, input_path, output_path)

analyse_pycg(project_name, input_path, output_path)

input_path = "data/pyanalyzer/" + project_name
analyse_pyanalyzer(project_name, input_path, output_path)

input_path = "data/enre19/" + project_name
analyse_enre19(project_name, input_path, output_path)

input_path = "data/pyanalyzer-cfg/" + project_name
analyse_pyanalyzercfg(project_name, input_path, output_path)

input_path = "result/" + project_name
analyse_callgraph(project_name, input_path, output_path)

input_path = "result/" + project_name + '/type4py/'
analyse_type4py(project_name, input_path, output_path)