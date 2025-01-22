# -*- coding: utf-8 -*-
# @File    :   convert_program_to_executable.py
# @Time    :   2025/01/22 11:07:13
# @Author  :   Qing 
# @Email   :   aqsz2526@outlook.com
######################### docstring ########################
'''
将 KQA 的 program 标注转为可执行的 python 代码
'''
from qdls.data import load_json
import os 
import pickle
from loguru import logger
from kopl.kopl import KoPLEngine, ValueClass

def load_engine():
    if os.path.exists("/home/qing/raid/paperwork/kgtool/data/kqa/engine.pkl"):
        with open("/home/qing/raid/paperwork/kgtool/data/kqa/engine.pkl", "rb") as f:
            engine = pickle.load(f)
    else:   
        engine = KoPLEngine(load_json("/home/qing/raid/paperwork/kgtool/data/kqa/kb_fixed.json"))
        with open("/home/qing/raid/paperwork/kgtool/data/kqa/engine.pkl", "wb") as f:
            pickle.dump(engine, f)   
            print("engine saved")
    return engine

# engine = load_engine()
engine = KoPLEngine(load_json("/home/qing/raid/paperwork/kgtool/data/kqa/full/kb.json"))

def convert_to_python(program):
    """
    Converts the program stack into the equivalent Python code.

    Args:
        program (list): A list of dictionaries representing the program.

    Returns:
        str: The final Python code as a string.
    """
    def escape_string(s: str) -> str:
        """Escape special characters in string."""
        # Replace single quotes with escaped single quotes
        return s.replace("'", "\\'")

    # Map function names in the program to their corresponding Python function calls
    def find_function_mapping(func_name):
        function_map = {
            # Basic entity operations
            "FindAll": lambda inputs: "engine.FindAll()",
            "Find": lambda inputs: f"engine.Find('{escape_string(inputs[0])}')",
            "FilterConcept": lambda deps, inputs: f"engine.FilterConcept({results[deps[0]]}, '{escape_string(inputs[0])}')",
            
            # Attribute filtering
            "FilterStr": lambda deps, inputs: f"engine.FilterStr({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            "FilterNum": lambda deps, inputs: f"engine.FilterNum({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            "FilterYear": lambda deps, inputs: f"engine.FilterYear({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            "FilterDate": lambda deps, inputs: f"engine.FilterDate({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            
            # Qualifier filtering
            "QFilterStr": lambda deps, inputs: f"engine.QFilterStr({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            "QFilterNum": lambda deps, inputs: f"engine.QFilterNum({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            "QFilterYear": lambda deps, inputs: f"engine.QFilterYear({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            "QFilterDate": lambda deps, inputs: f"engine.QFilterDate({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            
            # Relation operations
            "Relate": lambda deps, inputs: f"engine.Relate({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            
            # Set operations
            "And": lambda deps, _: f"engine.And({results[deps[0]]}, {results[deps[1]]})",
            "Or": lambda deps, _: f"engine.Or({results[deps[0]]}, {results[deps[1]]})",
            
            # Query operations
            "Count": lambda deps, _: f"engine.Count({results[deps[0]]})",
            "What": lambda deps, _: f"engine.QueryName({results[deps[0]]})",
            "QueryName": lambda deps, _: f"engine.QueryName({results[deps[0]]})",
            "QueryAttr": lambda deps, inputs: f"engine.QueryAttr({results[deps[0]]}, '{escape_string(inputs[0])}')",
            "QueryAttrUnderCondition": lambda deps, inputs: f"engine.QueryAttrUnderCondition({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            
            # Selection operations
            "SelectBetween": lambda deps, inputs: f"engine.SelectBetween({results[deps[0]]}, {results[deps[1]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            "SelectAmong": lambda deps, inputs: f"engine.SelectAmong({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            
            # Verification operations
            "VerifyStr": lambda deps, inputs: f"engine.VerifyStr({results[deps[0]]}, '{escape_string(inputs[0])}')",
            "VerifyNum": lambda deps, inputs: f"engine.VerifyNum({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            "VerifyYear": lambda deps, inputs: f"engine.VerifyYear({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            "VerifyDate": lambda deps, inputs: f"engine.VerifyDate({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
            
            # Relation and qualifier queries
            "QueryRelation": lambda deps, _: f"engine.QueryRelation({results[deps[0]]}, {results[deps[1]]})",
            "QueryAttrQualifier": lambda deps, inputs: f"engine.QueryAttrQualifier({results[deps[0]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}', '{escape_string(inputs[2])}')",
            "QueryRelationQualifier": lambda deps, inputs: f"engine.QueryRelationQualifier({results[deps[0]]}, {results[deps[1]]}, '{escape_string(inputs[0])}', '{escape_string(inputs[1])}')",
        }
        return function_map[func_name]

    results = []

    for step in program:
        func_name = step["function"]
        dependencies = step.get("dependencies", [])
        inputs = step.get("inputs", [])

        # Generate the corresponding Python code using the mapping
        func_mapper = find_function_mapping(func_name)
        if len(dependencies) > 0:
            result = func_mapper(dependencies, inputs)
        else:
            result = func_mapper(inputs)
        results.append(result)

    # The last item in `results` is the complete Python code for the program
    return results[-1]


def test():
    program = [
        {"function": "FindAll", "dependencies": [], "inputs": []},
        {"function": "FilterStr", "dependencies": [0], "inputs": ["Hornbostel-Sachs classification", "321.322-71"]},
        {"function": "FilterConcept", "dependencies": [1], "inputs": ["string instrument"]},
        {"function": "Find", "dependencies": [], "inputs": ["Charles Mingus Jr."]},
        {"function": "Relate", "dependencies": [3], "inputs": ["famous people", "backward"]},
        {"function": "FilterConcept", "dependencies": [4], "inputs": ["string instrument"]},
        {"function": "Or", "dependencies": [2, 5], "inputs": []},
        {"function": "Count", "dependencies": [6], "inputs": []}
    ]

    # Convert the program to Python code
    python_code = convert_to_python(program)
    print(python_code)
    print(eval(python_code))


def compare_result(ans, exec_result):

    def convert_to_str(value):
        """
        如果value是ValueClass，则转换为字符串; 如果是带有 unit 的，则返回 tuple (num, unit)
        如果不是直接str

        """
        if not isinstance(value, ValueClass):
            return str(value)
        
        if value.type == 'string':
            return value.value
        elif value.type == 'quantity':
            if value.value - int(value.value) < 1e-5:
                v = int(value.value)
            else:
                v = value.value
            # return '{} {}'.format(v, value.unit) if value.unit != '1' else str(v)   # 修改：数字保留一位
            return float(v), value.unit if value.unit != '1' else None
        elif value.type == 'year':
            return str(value.value)
        elif value.type == 'date':
            return value.value.isoformat()
        
    ##########################

    def eq(ans, exec_result): 
        """ 如果执行结果是 tuple，则表示是数量，需要比较数量和单位  
            如果 unit 是 None 表示单位是 1 则 ans 应该对应 ""
        """
        s = convert_to_str(exec_result)
        if isinstance(s, tuple):
            num, *unit = ans.split(" ")
            unit = " ".join(unit)
            return float(num) == s[0] and (unit == s[1] or (unit == "" and s[1] is None)) 
        else:
            return ans == s

    if isinstance(exec_result, list):
        if len(exec_result) == 1:
            exec_result = exec_result[0] 
        elif len(exec_result) == 0:
            exec_result = "Empty"
        else:
            return any( eq(ans, r) for r in exec_result)  # gold answer 只有一个
        
    if eq(ans, exec_result):
        return True
    else:
        logger.info(f"ans: {ans}, exec_result: {exec_result}")  
        return False


def validate_all_program(file):
    from tqdm import tqdm
    data = load_json(file)
    n = len(data)
    cnt = 0 
    for item in tqdm(data):
        program = item["program"]
        ans = item["answer"]
        python_code = convert_to_python(program)

        exec_result = eval(python_code)
        if compare_result(ans, exec_result):
            cnt += 1
        else:
            print(item['sample_id'])
            print(python_code)
            # print(item['cypher_match'])

            # print(item)

    print(f"validate {cnt}/{n} programs, accuracy: {cnt/n}")

if __name__ == "__main__":
    # validate_all_program("/home/qing/raid/paperwork/kgtool/data/kqa/split/val_3k.json")   # validate 2988/3000 programs, accuracy: 0.996
    # validate_all_program("/home/qing/raid/paperwork/kgtool/data/kqa/split/test_8k.json")  # validate 8773/8797 programs, accuracy: 0.9972717972035922
    validate_all_program("/home/qing/raid/paperwork/kgtool/data/kqa/full/train.json")     # validate 94029/94376 programs, accuracy: 0.996323217767229

