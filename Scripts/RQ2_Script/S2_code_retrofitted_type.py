
import glob, os, ast, astor
import json
import csv
import astunparse
from asttokens import ASTTokens

import codegen


if __name__ == '__main__':

    project_path_list = ["..\Data\RQ2\micro-benchmark B\Benchmark-collectedbyPyCG\args\assigned_call"]  #You should modify the paths within this list to the paths of the projects you intend to analyze.
    for index_path, project_path in enumerate(project_path_list):
        project_file_list = [f for f in glob.glob(f'{project_path}/**/*.json', recursive=True)]
        for index, fp in enumerate(project_file_list):
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    dirname, filename = os.path.split(fp)
                    json_path_list = fp.split("testcode\\")[-1].split("\\")
                    py_path_dir = "E:\\"
                    for json_index, json_path in enumerate(json_path_list):
                        if json_index != len(json_path_list) - 1:
                            py_path_dir = os.path.join(py_path_dir, json_path)
                    read_py_path = py_path_dir + "\\" + filename.split(".")[0] + ".py"
                    save_py_path = dirname + "\\" + filename.split(".")[0] + ".py"
                    project_dump = json.loads(f.read())
                    funcs_list = project_dump.get("response").get("funcs")
                    class_list = project_dump.get("response").get("classes")
                    for class_item in class_list:
                        class_funcs_list = class_item.get("funcs")
                        funcs_list.extend(class_funcs_list)
                    with open(read_py_path, "r", encoding='utf-8', errors='replace') as py_fp:
                        ast_node = ast.parse(py_fp.read())
                        # atok = ASTTokens(py_fp.read(), parse=True)
                        # ast_node = atok.tree
                        for item in ast.walk(ast_node):
                            if isinstance(item, ast.FunctionDef):
                                for funcs_obj in funcs_list:
                                    if item.name == funcs_obj.get("name"):
                                        for arg in item.args.args:
                                            try:
                                                arg_type = funcs_obj.get("params_p").get(arg.arg)[0][0]
                                            except (IndexError, TypeError):
                                                arg_type = None
                                            if arg_type:
                                                arg.annotation = ast.Name(id=arg_type, ctx=ast.Load())
                                        try:
                                            return_type = funcs_obj.get("ret_type_p")[0][0]
                                        except (IndexError, TypeError):
                                            return_type = None
                                        if return_type:
                                            item.returns = ast.Name(id=return_type, ctx=ast.Load())
                                        break
                        with open(save_py_path, "w", encoding='utf-8') as py_w_fp:
                            py_w_fp.write(ast.unparse(ast_node))
                            print("save_py_path=",save_py_path)
                except Exception as e:
                    with open("errors.log", "a") as f2:
                        print("error")
                        f2.write(str(e))
