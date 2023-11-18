import json
import argparse
import re

import understand


def contain(keyword, raw):
    return bool(re.search(r'(^| )%s' % keyword, raw))


def Entity(entityID, entityName, entityType, entityFile=None,
           startLine=-1, startColumn=-1, endColumn=-1, endLine=-1):
    entity = dict()
    location = dict()
    entity['id'] = entityID
    entity['qualifiedName'] = entityName.replace('\\', '/')
    entity['category'] = entityType

    location['startLine'] = startLine
    location['startColumn'] = startColumn
    location['endColumn'] = endColumn
    location['endLine'] = endLine
    entity['location'] = location
    if entityFile is not None:
        entity['file'] = entityFile.replace('\\', '/')

    return entity


def Dependency(dependencyType, dependencySrcID, dependencydestID,
               startLine=-1, startColumn=-1):
    dependency = dict()
    values = dict()
    location = dict()

    dependency['src'] = dependencySrcID
    dependency['dest'] = dependencydestID

    values['kind'] = dependencyType
    dependency['values'] = values

    location['startLine'] = startLine
    location['startCol'] = startColumn

    dependency['location'] = location
    return dependency


def outputAll(entity_list: list, relation_list: list, json_path: str, projectname: str):
    file = dict()

    file["entities"] = entity_list
    file["relations"] = relation_list

    dependency_str = json.dumps(file, indent=4)
    with open(json_path, 'w') as json_file:
        json_file.write(dependency_str)


def output(info_list: list, json_path: str, type: str, projectname: str):
    file = dict()

    file[type] = info_list

    dependency_str = json.dumps(file, indent=4)
    with open(json_path, 'w') as json_file:
        json_file.write(dependency_str)


# Usage
parser = argparse.ArgumentParser()
parser.add_argument('lang', help='Sepcify the target language:cpp, java, python, js')
parser.add_argument('project', help='Specify the project name')
parser.add_argument('dbpath', help='Specify the database path')
parser.add_argument('output', help='Specify the output path')
parser.add_argument('prepath', help='Specify the path your project in')
parser.add_argument('-p', help='only save a file containing entities and relations',
                    action=argparse.BooleanOptionalAction)
args = parser.parse_args()

print_mode = args.p
lang = args.lang

try:
    ['cpp', 'java', 'python', 'js'].index(lang)
except:
    raise ValueError(
        f'Invalid lang {lang}, only support cpp / java / python')

project_name = args.project
database_path = args.dbpath + project_name + '.und'
output_path = args.output + project_name + '/'

print('Openning udb file...')
db = understand.open(database_path)

ent_list = []

# Extract file entities first
print('Exporting File entities...')
file_count = 0
for ent in db.ents('File'):
    if (ent.language() == 'C++') | (ent.language() == 'C') | (ent.language() == 'Java') | \
            (ent.language() == 'Python') | (ent.language() == 'Web'):
        ent_list.append(Entity(ent.id(), ent.relname(), 'File'))
        file_count += 1
print(f'Total {file_count} files are successfully exported')

print('Exporting entities other that File...')
regular_count = 0

# Package, not belonging to any real files, worth process separately
for ent in db.ents('Package'):
    if (ent.language() == 'Java') | (ent.language() == 'Python'):
        # Assign Packages to a virtual file to fulfill db schema
        ent_list.append(Entity(ent.id(), ent.longname(), ent.kindname()));
        regular_count += 1

for ent in db.ents('Namespace'):
    if (ent.language() == 'C++') | (ent.language() == 'C'):
        ent_list.append(Entity(ent.id(), ent.longname(), ent.kindname()))
        regular_count += 1

# Filter entities other than file
unseen_entity_type = set()

select = "~File ~Package ~Unresolved ~Implicit ~Unknown"
if lang == "cpp":
    select = "~File ~Package ~Namespace ~Unresolved ~Implicit ~Unknown"
for ent in db.ents(select):
    if (ent.language() == 'C++') | (ent.language() == 'C') | \
            (ent.language() == 'Java') | (ent.language() == 'Python') | (ent.language() == 'Web'):
        # Although a suffix 's' is added, there should be only
        # one entry that matches the condition
        decls = ent.refs('Definein')
        if decls:
            # Normal entities should have a ref definein contains location
            # about where this entity is defined
            line = decls[0].line()
            start_column = decls[0].column() + 1
            end_column = start_column + len(ent.simplename())
            ent_list.append(
                Entity(ent.id(), ent.longname(), ent.kindname(), decls[0].file().relname(), line, start_column,
                       end_column))
            regular_count += 1
        else:
            unseen_entity_type.add(ent.kindname())
            ent_list.append(Entity(ent.id(), ent.longname(), ent.kindname()))

rel_list = []

print('Exporting relations...')
rel_count = 0
for ent in db.ents():
    if (ent.language() == 'C++') | (ent.language() == 'C') | \
            (ent.language() == 'Java') | (ent.language() == 'Python') | (ent.language() == 'Web'):
        for ref in ent.refs('~End', '~Unknown ~Unresolved ~Implicit'):
            if ref.isforward():
                rel_list.append(
                    Dependency(ref.kind().longname(), ref.scope().id(), ref.ent().id(), ref.line(), ref.column()))
                rel_count += 1

print("unseen entity type: ")
print(unseen_entity_type)

print(f'Total {regular_count} entities are successfully exported')
print(f'Total {rel_count} relations are successfully exported')

print('Saving results to the file...')
output(ent_list, output_path + "Understand_" + project_name + "_entity.json", 'entity', project_name)
output(rel_list, output_path + "Understand_" + project_name + "_dependency.json", 'dependency', project_name)
