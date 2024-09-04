from collections import Counter
from frozendict import frozendict

def json_process(item):
    if isinstance(item, dict):
        return frozendict((key,json_process(value)) for key, value in item.items())
    if isinstance(item, list):
        return frozendict(Counter(json_process(x) for x in item))
    else:
        return item

def json_compare(a,b):
    return json_process(a) == json_process(b)

