from typing import List, Tuple, Optional, Dict, Any
from typing_extensions import TypedDict
from dataclasses import dataclass
from kopl.kopl import KoPLEngine

class EntityTuple(TypedDict):
    ids: List[str]
    triples: Optional[List[Dict[str, Any]]]

@dataclass
class KoPLTools:
    """Collection of KoPL API tools for knowledge base operations"""
    
    def __init__(self, engine: KoPLEngine):
        self.engine = engine

    def find(self, name: str) -> Tuple[List[str], None]:
        """Find all entities with a specific name"""
        return self.engine.Find(name)

    def find_all(self) -> Tuple[List[str], None]:
        """Returns all entities in the knowledge base"""
        return self.engine.FindAll()

    def filter_concept(self, entities: EntityTuple, concept_name: str) -> Tuple[List[str], List]:
        """Filter entities by a specific concept/type"""
        return self.engine.FilterConcept(entities, concept_name)

    def filter_str(self, entities: EntityTuple, key: str, value: str) -> Tuple[List[str], List]:
        """Filter entities by string attribute"""
        return self.engine.FilterStr(entities, key, value)

    def filter_num(self, entities: EntityTuple, key: str, value: str, op: str) -> Tuple[List[str], List]:
        """Filter entities by numeric attribute
        
        Args:
            entities: Entity tuple to filter
            key: Attribute key
            value: Numeric value to compare against
            op: Comparison operator ('=', '!=', '<', '>')
        """
        return self.engine.FilterNum(entities, key, value, op)

    def filter_date(self, entities: EntityTuple, key: str, value: str, op: str) -> Tuple[List[str], List]:
        """Filter entities by date attribute (YYYY-MM-DD format)"""
        return self.engine.FilterDate(entities, key, value, op)

    def filter_year(self, entities: EntityTuple, key: str, value: str, op: str) -> Tuple[List[str], List]:
        """Filter entities by year attribute (YYYY format)"""
        return self.engine.FilterYear(entities, key, value, op)

    def query_attr(self, entities: EntityTuple, key: str) -> List[Any]:
        """Query attribute values for given entities"""
        return self.engine.QueryAttr(entities, key)

    def query_attr_qualifier(self, entities: EntityTuple, key: str, value: str, qkey: str) -> List[Any]:
        """Query qualifier values for specific attribute values"""
        return self.engine.QueryAttrQualifier(entities, key, value, qkey)

    def query_attr_under_condition(self, entities: EntityTuple, key: str, qkey: str, qvalue: str) -> List[Any]:
        """Query attribute values under specific qualifier conditions"""
        return self.engine.QueryAttrUnderCondition(entities, key, qkey, qvalue)

    def query_relation(self, s_entities: EntityTuple, t_entities: EntityTuple) -> List[str]:
        """Query relations between two sets of entities"""
        return self.engine.QueryRelation(s_entities, t_entities)

    def query_relation_qualifier(self, s_entities: EntityTuple, t_entities: EntityTuple, 
                               relation: str, qkey: str) -> List[Any]:
        """Query qualifier values for specific relations"""
        return self.engine.QueryRelationQualifier(s_entities, t_entities, relation, qkey)

    def relate(self, entities: EntityTuple, relation: str, direction: str) -> Tuple[List[str], List]:
        """Find entities related to input entities by a specific relation
        
        Args:
            entities: Source entities
            relation: Relation name
            direction: Either 'forward' or 'backward'
        """
        return self.engine.Relate(entities, relation, direction)

    def select_among(self, entities: EntityTuple, key: str, op: str) -> List[str]:
        """Select entities with largest/smallest attribute values
        
        Args:
            entities: Input entities
            key: Attribute key to compare
            op: Either 'largest' or 'smallest'
        """
        return self.engine.SelectAmong(entities, key, op)

    def select_between(self, l_entities: EntityTuple, r_entities: EntityTuple, 
                      key: str, op: str) -> str:
        """Compare two entities based on numeric attribute
        
        Args:
            l_entities: First entity tuple
            r_entities: Second entity tuple
            key: Attribute key to compare
            op: Either 'less' or 'greater'
        """
        return self.engine.SelectBetween(l_entities, r_entities, key, op)

    def and_op(self, l_entities: EntityTuple, r_entities: EntityTuple) -> Tuple[List[str], None]:
        """Get intersection of two entity sets"""
        return self.engine.And(l_entities, r_entities)

    def or_op(self, l_entities: EntityTuple, r_entities: EntityTuple) -> Tuple[List[str], None]:
        """Get union of two entity sets"""
        return self.engine.Or(l_entities, r_entities)

    def count(self, entities: EntityTuple) -> int:
        """Count number of entities"""
        return self.engine.Count(entities)

    def verify_str(self, s_value: List[Any], t_value: str) -> str:
        """Verify string values against target value
        Returns: 'yes', 'no', or 'not sure'
        """
        return self.engine.VerifyStr(s_value, t_value)

    def verify_num(self, s_value: List[Any], t_value: str, op: str) -> str:
        """Verify numeric values against target value
        Returns: 'yes', 'no', or 'not sure'
        """
        return self.engine.VerifyNum(s_value, t_value, op)

    def verify_date(self, s_value: List[Any], t_value: str, op: str) -> str:
        """Verify date values against target value (YYYY-MM-DD format)
        Returns: 'yes', 'no', or 'not sure'
        """
        return self.engine.VerifyDate(s_value, t_value, op)

    def verify_year(self, s_value: List[Any], t_value: str, op: str) -> str:
        """Verify year values against target value (YYYY format)
        Returns: 'yes', 'no', or 'not sure'
        """
        return self.engine.VerifyYear(s_value, t_value, op)

    def q_filter_str(self, entities: EntityTuple, qkey: str, qvalue: str) -> Tuple[List[str], List]:
        """Filter entities by string qualifier value"""
        return self.engine.QFilterStr(entities, qkey, qvalue)

    def q_filter_num(self, entities: EntityTuple, qkey: str, qvalue: str, op: str) -> Tuple[List[str], List]:
        """Filter entities by numeric qualifier value"""
        return self.engine.QFilterNum(entities, qkey, qvalue, op)

    def q_filter_date(self, entities: EntityTuple, qkey: str, qvalue: str, op: str) -> Tuple[List[str], List]:
        """Filter entities by date qualifier value (YYYY-MM-DD format)"""
        return self.engine.QFilterDate(entities, qkey, qvalue, op)

    def q_filter_year(self, entities: EntityTuple, qkey: str, qvalue: str, op: str) -> Tuple[List[str], List]:
        """Filter entities by year qualifier value (YYYY format)"""
        return self.engine.QFilterYear(entities, qkey, qvalue, op) 