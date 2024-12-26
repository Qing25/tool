
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

            R.append(s)
        save_json(R, file.replace(".json", "_new.json"))


    
if __name__ == "__main__":
    # merge_sampled_data()

    pass 