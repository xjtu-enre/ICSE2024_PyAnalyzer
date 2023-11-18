import json
import os


def execute(content: dict):
    commandList = [content['script'], content['language'][0], content['project'][0],
                   content['input_path'], content['output_path'], content['field_separator']]
    for iter in range(len(content['project'])):
        commandList[1:3] = content['language'][iter], content['project'][iter]

        command = " ".join(commandList)

        os.system(command)


if __name__ == "__main__":

    command = 'data/command.json'
    with open(command, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for key in data.keys():
        value = data[key]
        execute(value)
