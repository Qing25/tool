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
import pickle
from qdls.data import load_json, save_json
# import chattool 
# API_URL = "https://api.chatanywhere.tech/v1"
# API_KEY = os.environ.get('CHATANY_API_KEY', None) # local vllm set to "" 
# chattool.api_base = API_URL
# chattool.api_key = API_KEY

from kopl.kopl import KoPLEngine

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

engine = load_engine()
print(type(engine))

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

def fx():
    ans = engine.Count(
        engine.Or(
            engine.FilterConcept(
                engine.FilterStr(
                    engine.FindAll(),
                    key='Hornbostel-Sachs classification',
                    value='321.322-71'
                ),
                concept_name='string instrument'
            ),
            engine.FilterConcept(
                engine.Relate(
                    engine.Find('Charles Mingus Jr.'),
                    relation='famous people',
                    direction='backward'
                ),
                concept_name='string instrument'
            )
        )
    )
    print(ans)


def test2():
    entities_0 = engine.Find("Johann Sebastian Bach")
    entities_1 = engine.FindAll()
    filtered_entities_2 = engine.FilterStr(entities_0, "British Museum person-institution", "64954")
    filtered_entities_3 = engine.FilterStr(entities_1, "Hornbostel-Sachs classification", "321.322-71")
    related_entities_4 = engine.Relate(filtered_entities_2, "famous people", "backward")
    filtered_entities_5 = engine.FilterConcept(filtered_entities_3, "bowed string instrument")
    filtered_entities_6 = engine.FilterConcept(related_entities_4, "bowed string instrument")
    union_7 = engine.Or(filtered_entities_6, filtered_entities_5)
    count_8 = engine.Count(union_7)
    ans = count_8  
    print(ans)

    ans = engine.Count(
            engine.Or(
                engine.FilterConcept(
                    engine.Relate(
                        engine.FilterStr(
                            engine.Find('Johann Sebastian Bach'),
                            key='British Museum person-institution',
                            value='64954'
                        ),
                        relation='famous people',
                        direction='backward'
                    ),
                    concept_name='bowed string instrument'
                ),
                engine.FilterConcept(
                    engine.FilterStr(
                        engine.FindAll(),
                        key='Hornbostel-Sachs classification',
                        value='321.322-71'
                    ),
                    concept_name='bowed string instrument'
                )
            )
        )
    print(ans)



def debug():
    program = [
        {'function': 'Find', 'dependencies': [], 'inputs': ['Mary J. Blige']}, 
        {'function': 'Relate', 'dependencies': [0], 'inputs': ['famous people', 'backward']}, 
        {'function': 'FilterConcept', 'dependencies': [1], 'inputs': ['mechanical wave']}, 
        {'function': 'What', 'dependencies': [2], 'inputs': []}]
    engine.QueryName(engine.FilterConcept(engine.Relate(engine.Find('Mary J. Blige'), 'famous people', 'backward'), 'mechanical wave'))

if __name__ == '__main__':
    # pass 
    # test_demo()
    # print(engine.Find('Washington University in St. Louis'))
    # fx()
    test2()