import csv
import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, List, Set, Iterable, Optional


def align_test_dir(dir: Path):
    for sub_dir in dir.absolute().iterdir():
        os.chdir(sub_dir)
        for case in sub_dir.iterdir():
            case_name = case.name
            if case.is_dir():
                subprocess.call(
                    f"__main__.exe {case} --cfg --cg --builtins F:\\Master\\Python\\AIDep-py\\test\\builtins", shell=True)

                subprocess.call(
                    "pycg {} -o {}"
                        .format(case.joinpath("main.py"), case.joinpath("pycg-callgraph.json")), shell=True)
                case.joinpath("pycg-callgraph.json") \
                    .write_text(case.joinpath("pycg-callgraph.json")
                                .read_text().replace(f"{case_name}\\\\", ""))


import re

lambda_pattern = "(.*)\\(\d+\\)$"
compiled_pattern = re.compile(lambda_pattern)
pyanalyzerCall = int
PycgCall = int
SameCall = int


def remove_lambda_postfix(longname: str) -> Optional[str]:
    if matched := re.match(compiled_pattern, longname):
        removed_postfix = matched.group(1)
        return removed_postfix
    return None


def create_lambda_dict(case_dir: Path, pyanalyzer_file: Path) -> Dict[str, int]:
    dep = json.loads(pyanalyzer_file.read_text())
    entities = dep["variables"]
    id_mapping = dict()
    lambda_funcs = []

    for ent in entities:
        if ent["category"] == "AnonymousFunction":
            lambda_funcs.append(ent)
        id_mapping[ent["id"]] = ent

    lambda_func_dict = dict()
    for index, func in enumerate(lambda_funcs):
        lambda_func_dict[func["qualifiedName"].removeprefix(f"{case_dir.name}.")] = index + 1

    return lambda_func_dict


def build_pyanalyzer_call(pyanalyzer_file: Path, top_dir: Path) -> Set[Tuple[str, str]]:
    def translate_lambda_repr(func: str) -> str:
        if prefix := remove_lambda_postfix(func):
            lambda_index = lambda_func_dict[func]
            return prefix + f"<lambda{lambda_index}>"
        else:
            return func

    dep = json.loads(pyanalyzer_file.read_text())
    entities = dep["variables"]
    relations = dep["cells"]
    id_mapping = dict()
    ret = set()
    lambda_funcs = []
    for ent in entities:
        if ent["category"] == "AnonymousFunction":
            lambda_funcs.append(ent)
        id_mapping[ent["id"]] = ent
    lambda_funcs.sort(key=lambda e: e["location"]["startLine"])
    lambda_func_dict = dict()
    for index, func in enumerate(lambda_funcs):
        lambda_func_dict[func["qualifiedName"].removeprefix(f"{top_dir.name}.")] = index + 1
    for rel in relations:
        values = rel["values"]
        kind = values["kind"]
        from_id = rel["src"]
        to_id = rel["dest"]
        src_ent = id_mapping[from_id]
        if src_ent["File"].endswith("builtins"):
            continue
        if kind == "Call":
            caller = id_mapping[from_id]["qualifiedName"]
            callee = id_mapping[to_id]
            callee_qualified_name = callee["qualifiedName"]
            ret.add((caller.removeprefix(f"{top_dir.name}."), callee_qualified_name.removeprefix(f"{top_dir.name}.")))
            if "resolved" in values:
                for resolve_id in values["resolved"]:
                    callee = id_mapping[resolve_id]
                    callee_qualified_name = callee["qualifiedName"]
                    if "builtins.__init__" in callee_qualified_name:
                        continue
                    ret.add((caller.removeprefix(f"{top_dir.name}."),
                             callee_qualified_name.removeprefix(f"{top_dir.name}.")))

    return set(map(lambda rel: (translate_lambda_repr(rel[0]), translate_lambda_repr(rel[1])), ret))


def strip_case_name(case_name: str, call_graph: Set[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    return set(
        map(lambda rel: (rel[0].removeprefix(f"{case_name}."), rel[1].removeprefix(f"{case_name}.")), call_graph))


def get_call_relation(case_dir: Path, pycg_file: Path, pyanalyzer_dep: Path = None) -> Set[Tuple[str, str]]:
    def translate_lambda_repr(func: str) -> str:
        if prefix := remove_lambda_postfix(func):
            lambda_index = lambda_func_dict[func]
            return prefix + f"<lambda{lambda_index}>"
        else:
            return func

    ret = set()
    dep = json.loads(pycg_file.read_text())
    for key, value in dep.items():
        if pyanalyzer_dep and key.startswith("builtins"):
            continue
        for callee in value:
            if "__init__" in callee:
                continue
            ret.add((key, callee
                     .replace("<builtin>", "builtins")
                     .replace("<**PyDict**>", "builtins.dict")
                     .replace("<**PyStr**>", "builtins.str")))
    if pyanalyzer_dep:
        lambda_func_dict = create_lambda_dict(case_dir, pyanalyzer_dep)
        striped_case_prefix = strip_case_name(case_dir.name, ret)
        return set(map(lambda rel: (translate_lambda_repr(rel[0]), translate_lambda_repr(rel[1])), striped_case_prefix))
    else:
        return ret


CallRelation = Set[Tuple[str, str]]


def test_if_same_call_relation(case_dir: Path, ground_truth_file: Path, pyanalyzer_file: Path, pyanalyzer_cg: Path,
                               pycg_path: Path) -> Tuple[
    CallRelation, CallRelation, CallRelation, CallRelation]:
    pyanalyzer_call_relation = build_pyanalyzer_call(pyanalyzer_file, case_dir)
    pyanalyzer_resolved_call_relation = get_call_relation(case_dir, pyanalyzer_cg, pyanalyzer_file)
    ground_truth_call_relation = get_call_relation(case_dir, ground_truth_file)
    pycg_call_relation = get_call_relation(case_dir, pycg_path)
    return pyanalyzer_call_relation, pyanalyzer_resolved_call_relation, pycg_call_relation, ground_truth_call_relation


@dataclass
class CompareItem:
    case: str
    pyanalyzer_and_truth: int
    pyanalyzer_resolved_and_truth: int
    pycg_and_truth: int
    pyanalyzer_count: int
    pyanalyzer_resolved_count: int
    pycg_count: int
    truth_count: int
    pyanalyzer_call_graph: CallRelation
    pyanalyzer_call_graph_resolved: CallRelation
    pycg_call_graph: CallRelation
    truth: CallRelation


def dump_call_graph_compare(out_name: str, rows: Iterable[CompareItem]) -> None:
    with open(out_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["case", "pyanalyzer(all)&truth", "pyanalyzer(all)", "pyanalyzer(resolved) & truth", "pyanalyzer(resolved)",
             "pycg & truth","pycg", "truth",
             "pyanalyzer data(all)", "pyanalyzer data(resolved)", "truth data", "pyanalyzer(resolved) - truth",
             "truth - pyanalyzer(resolved)", "pycg - truth", "truth - pycg"])
        writer.writerows(
            (row.case, row.pyanalyzer_and_truth, row.pyanalyzer_count, row.pyanalyzer_resolved_and_truth, row.pyanalyzer_resolved_count,
             row.pycg_and_truth, row.pycg_count, row.truth_count,
             row.pyanalyzer_call_graph, row.pyanalyzer_call_graph_resolved, row.truth,
             row.pyanalyzer_call_graph_resolved.difference(row.truth),
             row.truth.difference(row.pyanalyzer_call_graph_resolved), row.pycg_call_graph.difference(row.truth),
             row.truth.difference(row.pycg_call_graph))
            for row in rows)


def create_compare_item(case_dir: str, pyanalyzer: CallRelation, pyanalyzer_cg: CallRelation, pycg_cg: CallRelation,
                        truth: CallRelation) -> CompareItem:
    pyanalyzer_and_truth = pyanalyzer.intersection(truth)
    pyanalyzer_resolved_and_truth = pyanalyzer_cg.intersection(truth)
    pycg_and_truth = pycg_cg.intersection(truth)
    return CompareItem(case=case_dir,
                       pyanalyzer_resolved_and_truth=len(pyanalyzer_resolved_and_truth),
                       pyanalyzer_and_truth=len(pyanalyzer_and_truth),
                       pycg_and_truth=len(pycg_and_truth),
                       pyanalyzer_resolved_count=len(pyanalyzer_cg),
                       pyanalyzer_count=len(pyanalyzer),
                       pycg_count=len(pycg_cg),
                       truth_count=len(truth),
                       pyanalyzer_call_graph=pyanalyzer,
                       pyanalyzer_call_graph_resolved=pyanalyzer_cg,
                       pycg_call_graph=pycg_cg,
                       truth=truth)


def gen_precision_for_all(snippets: Path, prefix: str):
    rows: List[CompareItem] = []
    for sub_dir in snippets.iterdir():
        for case in sub_dir.iterdir():
            if not case.is_dir():
                continue
            pyanalyzer_path = sub_dir.joinpath(f"{case.name}-report-pyanalyzer.json")
            pyanalyzer_resolved_call_graph_path = sub_dir.joinpath(f"{case.name}-call-graph-pyanalyzer.json")
            ground_truth_path = case.joinpath("callgraph.json")
            pycg_path = case.joinpath(f"pycg-callgraph.json")
            pyanalyzer, pyanalyzer_cg, pycg_cg, ground_truth_cg = test_if_same_call_relation(case, ground_truth_path, pyanalyzer_path,
                                                                                 pyanalyzer_resolved_call_graph_path,
                                                                                 pycg_path)
            rows.append(create_compare_item(str(case.relative_to(snippets)), pyanalyzer, pyanalyzer_cg, pycg_cg, ground_truth_cg))
    dump_call_graph_compare(f"{prefix}-precision.csv", rows)
    unresolved_rows = (r for r in rows if r.pyanalyzer_resolved_and_truth != r.truth_count)
    dump_call_graph_compare(f"{prefix}-unresolved_cases.csv", unresolved_rows)


def entry():
    pycg_snippets = Path("Benchmark-collectedbyPyCG")
    pyanalyzer_snippets = Path("Benchmark-newlyaddedbyPyAnalyzer")
    pyanalyzer_case_dir = pyanalyzer_snippets.absolute()
    pycg_case_dir = pycg_snippets.absolute()
    align_test_dir(pyanalyzer_case_dir)
    os.chdir(pyanalyzer_case_dir.parent)

    # gen_precision_for_all(pyanalyzer_case_dir, "pyanalyzer-benchmark")
    # align_test_dir(pycg_case_dir)
    gen_precision_for_all(pycg_case_dir, "pycg-benchmark")


if __name__ == "__main__":
    entry()
