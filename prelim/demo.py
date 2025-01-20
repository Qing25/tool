# -*- coding: utf-8 -*-
# @File    :   demo.py
# @Time    :   2024/12/26 15:42:15
# @Author  :   Qing 
# @Email   :   aqsz2526@outlook.com
######################### docstring ########################
'''
LLM 调用 KoPL 的 API 进行推理
'''
import os 
from qdls.data import load_json, save_json
# import chattool 
# API_URL = "https://api.chatanywhere.tech/v1"
# API_KEY = os.environ.get('CHATANY_API_KEY', None) # local vllm set to "" 
# chattool.api_base = API_URL
# chattool.api_key = API_KEY

from kopl.kopl import KoPLEngine

engine = KoPLEngine(load_json("/home/qing/raid/paperwork/kgtool/data/kqa/kb_fixed.json"))

def test_demo():
    # 问题 "Is there less area in DeKalb County (the one whose PermID is 5037043580) or Boulder County ?"
    # Find(DeKalb County).FilterStr(PermID,5037043580).Find(Boulder County).Or().Select(area,smallest,1,0).What() 
    ans = engine.SelectBetween(  
            engine.FilterStr(  # .FilterStr(PermID,5037043580)
                    engine.Find('DeKalb County'),  # Find(DeKalb County)
                    key='PermID',
                    value='5037043580'
            ),
            engine.Find('Boulder County'),  # Find(Boulder County)
            key='area',
            op='less'  # 'smallest' for minimum value
        )
    print(ans)


if __name__ == '__main__':
    # pass 
    test_demo()