import hashlib
all_tests = {}

for i in range(1,2):
    item_info = {}
    name = f'{i}'
    inp = open(f'{name}.in','rb').read()
    outp = open(f'{name}.out','rb').read()
    item_info["input_name"] = f'{name}.in'
    item_info["input_size"] = len(inp)
    item_info["output_name"] = f'{name}.out'
    item_info["output_md5"] = hashlib.md5(outp).hexdigest()
    item_info["output_size"] = len(outp)
    item_info["stripped_output_md5"] = hashlib.md5(outp.rstrip()).hexdigest()
    all_tests[str(i)] = item_info

info = {
    "test_case_number": 2,
    "spj": False,
    "test_cases": all_tests
}
import json
with open("info", "w") as f:
    json.dump(info, f)