
# -*- coding: utf-8 -*-
# @File    :   convert_kopl.py
# @Time    :   2024/12/26 14:25:00
# @Author  :   Qing 
# @Email   :   aqsz2526@outlook.com
######################### docstring ########################
'''
将 kopl 转为 tool 的格式
'''
######################### docstring ########################

import os
import json
import pandas as pd
from qdls.data import load_json, save_json

def merge_sampled_data():

    """ 将 program 的标注融合进 sampled 数据中 
    run once only
    """
    files = [
        "/home/qing/raid/paperwork/kgtool/data/kqa/sampled/sampled_50.json",
        "/home/qing/raid/paperwork/kgtool/data/kqa/sampled/sampled_100.json",
        "/home/qing/raid/paperwork/kgtool/data/kqa/sampled/sampled_200.json",
    ]
    full = load_json("/home/qing/raid/paperwork/kgtool/data/kqa/full/train.json")
    q2sample = { s['question']: s for s in full }
    for file in files:
        R = [] 
        sampled = load_json(file)
        for s in sampled:
            
            new = q2sample[s['question']]
            program = new['program']
            sample_id = new['sample_id']
            s['program'] = program
            s['sample_id'] = sample_id
            s['answer'] = new['answer']

            R.append(s)
        # save_json(R, file.replace(".json", "_new.json"))
        save_json(R, file)


def convert_valdata():
    """ 将 valdata 的标注融合进 sampled 数据中 
    run once only
    """
    valtest = load_json("/home/qing/raid/paperwork/aaai24/data/kqa/gqir/left_val.json")
    q2data = { s['question']: s for s in valtest }


    leftval = load_json("/home/qing/raid/paperwork/kgtool/data/kqa/split/left_val.json")

    for s in leftval:
        q = s['question']
        s.update(q2data[q])
    

    save_json(leftval, "/home/qing/raid/paperwork/kgtool/data/kqa/split/test_8k.json")

    merged_val = load_json("/home/qing/raid/paperwork/aaai24/data/kqa/merged/val.json")
    id2sample = { s['sample_id']: s for s in merged_val }
    val = load_json("/home/qing/raid/paperwork/kgtool/data/kqa/split/val.json")
    for s in val:
        m = id2sample[s['sample_id']]
        s['graphq_ir'] = m['graphq_ir']
        s['kopl'] = m['kopl']
        s['lambda-dcs'] = m['lambda-dcs']
    
    save_json(val, "/home/qing/raid/paperwork/kgtool/data/kqa/split/val_3k.json")

if __name__ == "__main__":
    # merge_sampled_data()
    convert_valdata()
    pass 