from collections import Counter
from frozendict import frozendict
import json

def json_process(item):
    if isinstance(item, dict):
        return frozendict((key,json_process(value)) for key, value in item.items())
    elif isinstance(item, list):
        return frozendict(Counter(json_process(x) for x in item))
    else:
        return item

def stdout_to_json(stdout):
    stdout = stdout.split('\n')
    stdout = ''.join(stdout[1:])
    stdout = json.loads(stdout)

    return stdout
    
def json_compare2(stdout,b):
    """Skips 1st line of stdout and compares with b"""
    return json_process(stdout_to_json(stdout)) == json_process(b)

