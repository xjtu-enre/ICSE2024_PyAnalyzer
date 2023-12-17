from collections import defaultdict
from typing import Sequence, Any, Dict

from pyanalyzer.cfg.Resolver import Resolver
from pyanalyzer.cfg.HeapObject import FunctionObject, InstanceMethodReference, ClassObject
from pyanalyzer.cfg.module_tree import ModuleSummary, Scene
from pyanalyzer.ent.entity import Function, Entity, Class


def from_summaries(summaries: Sequence[ModuleSummary]) -> str:
    ret = ""
    for summary in summaries:
        ret += f"{str(summary)}\n"
        for name, objs in summary.get_namespace().items():
            ret += f"\t{name}: "
            ret += ",".join(str(obj.representation()) for obj in objs)
            ret += "\n"

    return ret


def call_graph_representation(resolver: Resolver) -> Dict[str, Any]:
    call_graph_dict = defaultdict(list)
    call_graph = resolver.call_graph
    for source, invoke_targets in call_graph.graph.items():
        for target in invoke_targets:
            if isinstance(target, Class) and "builtins" not in target.longname.longname:
                continue
            call_graph_dict[source.longname.longname].append(target.longname.longname)
    return call_graph_dict
