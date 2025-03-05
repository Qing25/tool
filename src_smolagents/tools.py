# -*- coding: utf-8 -*-
# @File    :   tools.py
# @Time    :   2025/02/13 15:46:26
# @Author  :   Qing 
# @Email   :   aqsz2526@outlook.com
######################### docstring ########################
'''
    使用 smolagents 重构 kopl 的所有 tools 
'''

import os 
import pickle
from qdls.data import save_json,load_json
from loguru import logger   
from smolagents import tool
from typing import List, Tuple, Union
from qdls.kopl.kopl import ValueClass

from qdls.kopl.kopl import KoPLEngine

def load_or_create_engine(kb_path: str, pickle_path: str) -> KoPLEngine:
    """Load KB from pickle if exists, otherwise create and save"""
    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as f:
            engine = pickle.load(f)
        logger.info(f"Loaded KB from pickle file")
    else:
        engine = KoPLEngine(load_json(kb_path))
        with open(pickle_path, "wb") as f:
            pickle.dump(engine, f)
        logger.info(f"Saved KB to pickle file")
    return engine

KB_PATH = "/home/qing/raid/paperwork/kgtool/data/kqa/kb.json"
PICKLE_PATH = "/home/qing/raid/paperwork/kgtool/data/kqa/kb.pkl"

engine = load_or_create_engine(KB_PATH, PICKLE_PATH)

tools = [] 

EntityTuple = Tuple[List[str], Union[None, List[ValueClass]]]

@tool
def Find(name: str) -> str:
    """
    Find all entities with a specific name in the knowledge base

    Args:
        name: name of the entity
    Returns:
        :obj:`tuple`: a tuple of two elements, the first is a list of entity ids, the second is None
    """
    return engine.Find(name)

@tool
def FindAll() -> str:
    """
    Return all entities in the knowledge base

    Returns:
        str: A tuple of two elements, the first is a list of entity ids, the second is None
    """
    return engine.FindAll()

@tool
def FilterConcept(entities: EntityTuple, concept_name: str) -> str:
    """
    Find all entities that belong to a specific concept

    Args:
        entities: A tuple, first element is entity list, second is triple list
        concept_name: The given concept label
    
    Returns:
        str: A tuple of two elements, first is intersection of input entity sets, second is None
    """
    return engine.FilterConcept(entities, concept_name)

@tool
def FilterStr(entities: EntityTuple, key: str, value: str) -> str:
    """
    Filter entities based on string attribute key-value pairs

    Args:
        entities: A tuple, first element is entity list, second is triple list
        key: Attribute key
        value: Attribute value
    
    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.FilterStr(entities, key, value)

@tool
def FilterNum(entities: EntityTuple, key: str, value: str, op: str) -> str:
    """
    Filter entities based on numeric attribute key-value pairs with comparison operator

    Args:
        entities: A tuple, first element is entity list, second is triple list
        key: Attribute key
        value: Attribute value (numeric)
        op: Comparison operator, one of "=", "!=", "<", ">"
    
    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.FilterNum(entities, key, value, op)

@tool
def FilterYear(entities: EntityTuple, key: str, value: str, op: str) -> str:
    """
    Filter entities based on year attribute key-value pairs with comparison operator

    Args:
        entities: A tuple, first element is entity list, second is triple list
        key: Attribute key
        value: Attribute value (year)
        op: Comparison operator, one of "=", "!=", "<", ">"
    
    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.FilterYear(entities, key, value, op)

@tool
def FilterDate(entities: EntityTuple, key: str, value: str, op: str) -> str:
    """
    Filter entities based on date attribute key-value pairs with comparison operator

    Args:
        entities: A tuple, first element is entity list, second is triple list
        key: Attribute key
        value: Attribute value (date)
        op: Comparison operator, one of "=", "!=", "<", ">"
    
    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.FilterDate(entities, key, value, op)

@tool
def Relate(entities: EntityTuple, relation: str, direction: str) -> str:
    """
    Find all entities that have a specific relation with input entities

    Args:
        entities: A tuple, first element is entity list, second is None or triple list
        relation: Relation label
        direction: "forward" or "backward", indicating if input entities are head or tail

    Returns:
        str: A tuple of two elements, first is related entity list, second is triple list
    """
    return engine.Relate(entities, relation, direction)

@tool
def And(l_entities: EntityTuple, r_entities: EntityTuple) -> str:
    """
    Return intersection of two entity sets

    Args:
        l_entities: A tuple, first element is entity list, second is None or triple list
        r_entities: A tuple, first element is entity list, second is None or triple list

    Returns:
        str: A tuple of two elements, first is intersection of input sets, second is None
    """
    return engine.And(l_entities, r_entities)

@tool
def Or(l_entities: EntityTuple, r_entities: EntityTuple) -> str:
    """
    Return union of two entity sets

    Args:
        l_entities: A tuple, first element is entity list, second is None or triple list
        r_entities: A tuple, first element is entity list, second is None or triple list

    Returns:
        str: A tuple of two elements, first is union of input sets, second is None
    """
    return engine.Or(l_entities, r_entities)

@tool
def QueryName(entities: EntityTuple) -> str:
    """
    Query entity names

    Args:
        entities: A tuple, first element is entity list, second is None or triple list

    Returns:
        str: A list of strings, each corresponding to an entity name
    """
    return engine.QueryName(entities)

@tool
def Count(entities: EntityTuple) -> str:
    """
    Count number of entities in set

    Args:
        entities: A tuple, first element is entity list, second is None or triple list

    Returns:
        str: Integer count of entities
    """
    return engine.Count(entities)

@tool
def SelectBetween(l_entities: EntityTuple, r_entities: EntityTuple, key: str, op: str) -> str:
    """
    Select entity with larger/smaller attribute value between two entities

    Args:
        l_entities: A tuple, first element is entity list, second is None or triple list
        r_entities: A tuple, first element is entity list, second is None or triple list
        key: Attribute key requiring numeric value
        op: "less" or "greater" to select entity with smaller/larger value

    Returns:
        str: Name of the selected entity
    """
    return engine.SelectBetween(l_entities, r_entities, key, op)

@tool
def SelectAmong(entities: EntityTuple, key: str, op: str) -> str:
    """
    Select entities with smallest/largest attribute value from set

    Args:
        entities: A tuple, first element is entity list, second is None or triple list
        key: Attribute key requiring numeric value
        op: "smallest" or "largest" to select entities with min/max value

    Returns:
        str: List of entity names with min/max value
    """
    return engine.SelectAmong(entities, key, op)

@tool
def QueryAttr(entities: EntityTuple, key: str) -> str:
    """
    Query attribute values for entities

    Args:
        entities: A tuple, first element is entity list, second is None or triple list
        key: Attribute key to query

    Returns:
        str: List of attribute values
    """
    return engine.QueryAttr(entities, key)

@tool
def QueryAttrUnderCondition(entities: EntityTuple, key: str, qkey: str, qvalue: str) -> str:
    """
    Query attribute values under specific qualifier condition

    Args:
        entities: A tuple, first element is entity list, second is None or triple list
        key: Attribute key to query
        qkey: Qualifier key
        qvalue: Qualifier value

    Returns:
        str: List of attribute values meeting the qualifier condition
    """
    return engine.QueryAttrUnderCondition(entities, key, qkey, qvalue)

@tool
def VerifyStr(s_value: List[ValueClass], t_value: str) -> str:
    """
    Verify if attribute values equal given string

    Args:
        s_value: List of ValueClass instances from QueryAttr/QueryAttrUnderCondition
        t_value: Target string value to verify against

    Returns:
        str: "yes", "no", or "not sure" indicating if values match
    """
    return engine.VerifyStr(s_value, t_value)

@tool
def VerifyNum(s_value: List[ValueClass], t_value: str, op: str) -> str:
    """
    Verify if numeric attribute values satisfy comparison

    Args:
        s_value: List of ValueClass instances from QueryAttr/QueryAttrUnderCondition
        t_value: Target numeric value to verify against
        op: Comparison operator ("=", "!=", "<", ">")

    Returns:
        str: "yes", "no", or "not sure" indicating if comparison holds
    """
    return engine.VerifyNum(s_value, t_value, op)

@tool
def VerifyYear(s_value: List[ValueClass], t_value: str, op: str) -> str:
    """
    Verify if year attribute values satisfy comparison

    Args:
        s_value: List of ValueClass instances from QueryAttr/QueryAttrUnderCondition
        t_value: Target year value to verify against
        op: Comparison operator ("=", "!=", "<", ">")

    Returns:
        str: "yes", "no", or "not sure" indicating if comparison holds
    """
    return engine.VerifyYear(s_value, t_value, op)

@tool
def VerifyDate(s_value: List[ValueClass], t_value: str, op: str) -> str:
    """
    Verify if date attribute values satisfy comparison

    Args:
        s_value: List of ValueClass instances from QueryAttr/QueryAttrUnderCondition
        t_value: Target date value to verify against
        op: Comparison operator ("=", "!=", "<", ">")

    Returns:
        str: "yes", "no", or "not sure" indicating if comparison holds
    """
    return engine.VerifyDate(s_value, t_value, op)

@tool
def QueryRelation(s_entities: EntityTuple, t_entities: EntityTuple) -> str:
    """
    Query relations between two sets of entities

    Args:
        s_entities: A tuple, first element is source entity list, second is None or triple list
        t_entities: A tuple, first element is target entity list, second is None or triple list

    Returns:
        str: List of relation labels between the entities
    """
    return engine.QueryRelation(s_entities, t_entities)

@tool
def QueryAttrQualifier(entities: EntityTuple, key: str, value: str, qkey: str) -> str:
    """
    Query qualifier values for specific attribute

    Args:
        entities: A tuple, first element is entity list, second is None or triple list
        key: Attribute key
        value: Attribute value
        qkey: Qualifier key to query

    Returns:
        str: List of qualifier values
    """
    return engine.QueryAttrQualifier(entities, key, value, qkey)

@tool
def QueryRelationQualifier(s_entities: EntityTuple, t_entities: EntityTuple, relation: str, qkey: str) -> str:
    """
    Query qualifier values for specific relation between entities

    Args:
        s_entities: A tuple, first element is source entity list, second is None or triple list
        t_entities: A tuple, first element is target entity list, second is None or triple list
        relation: Relation label
        qkey: Qualifier key to query

    Returns:
        str: List of qualifier values
    """
    return engine.QueryRelationQualifier(s_entities, t_entities, relation, qkey)

@tool
def QFilterStr(entities: EntityTuple, qkey: str, qvalue: str) -> str:
    """
    Filter triples based on string qualifier key-value pairs

    Args:
        entities: A tuple, first element is entity list, second is triple list
        qkey: Qualifier key
        qvalue: Qualifier value (string)

    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.QFilterStr(entities, qkey, qvalue)

@tool
def QFilterNum(entities: EntityTuple, qkey: str, qvalue: str, op: str) -> str:
    """
    Filter triples based on numeric qualifier key-value pairs with comparison operator

    Args:
        entities: A tuple, first element is entity list, second is triple list
        qkey: Qualifier key
        qvalue: Qualifier value (numeric)
        op: Comparison operator, one of "=", "!=", "<", ">"

    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.QFilterNum(entities, qkey, qvalue, op)

@tool
def QFilterYear(entities: EntityTuple, qkey: str, qvalue: str, op: str) -> str:
    """
    Filter triples based on year qualifier key-value pairs with comparison operator

    Args:
        entities: A tuple, first element is entity list, second is triple list
        qkey: Qualifier key
        qvalue: Qualifier value (year)
        op: Comparison operator, one of "=", "!=", "<", ">"

    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.QFilterYear(entities, qkey, qvalue, op)

@tool
def QFilterDate(entities: EntityTuple, qkey: str, qvalue: str, op: str) -> str:
    """
    Filter triples based on date qualifier key-value pairs with comparison operator

    Args:
        entities: A tuple, first element is entity list, second is triple list
        qkey: Qualifier key
        qvalue: Qualifier value (date)
        op: Comparison operator, one of "=", "!=", "<", ">"

    Returns:
        str: A tuple of two elements, first is entity list, second is triple list
    """
    return engine.QFilterDate(entities, qkey, qvalue, op)

tools = [
    Find, FindAll, 
    FilterConcept, FilterStr, FilterNum, FilterYear, FilterDate,
    Relate, And, Or, 

    Count, SelectBetween, SelectAmong, 
    VerifyStr, VerifyNum, VerifyYear, VerifyDate, 
    QFilterStr, QFilterNum, QFilterYear, QFilterDate,
    QueryName, QueryAttr, QueryAttrUnderCondition, 
    QueryRelation, QueryAttrQualifier, QueryRelationQualifier,
]



if __name__ == "__main__":
    # print(Find("Obama"))
    print(QueryAttrUnderCondition({'entities': "(['Q495588'], None)", 'key': 'population', 'qkey': 'date', 'qvalue': '140305'}))
