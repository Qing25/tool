# -*- coding: utf-8 -*-
# @File    :   fix_kqa_kb.py
# @Time    :   2024/12/27 14:05:29
# @Author  :   Qing 
# @Email   :   aqsz2526@outlook.com
######################### docstring ########################
'''
1.
example kb 中 concept 对应的是subclassOf 
但是 kqa 的 kb.json 中 concept 对应的是 instanceOf

2.
解析实体的时候出错
  File "/site-packages/kopl/data.py", line 39, in __init__
    'relation': rel_info['relation'],
                ~~~~~~~~^^^^^^^^^^^^
KeyError: 'relation'

'''

from qdls.data import load_json, save_json

kb = load_json("/home/qing/raid/paperwork/kgtool/data/kqa/kb.json")

# for qid, v in kb['entities'].items():
#     save_json(v, f"./{qid}.json")
#     exit()

# 将 predicate 换成 relation
for qid, v in kb['entities'].items():
    for i, rel_info in enumerate(v['relations']):
        kb['entities'][qid]['relations'][i]['relation'] = rel_info['predicate']
        kb['entities'][qid]['relations'][i].pop('predicate')

# 将 instanceOf 换成 subclassOf
for qid, v in kb['concepts'].items():
    kb['concepts'][qid]['subclassOf'] = v['instanceOf']
    kb['concepts'][qid].pop('instanceOf')




save_json(kb, "/home/qing/raid/paperwork/kgtool/data/kqa/kb_fixed.json")