from typing import List, Tuple, Optional, Dict, Any, Sequence
from typing_extensions import TypedDict, Annotated
from dataclasses import dataclass
from autogen_core.tools import FunctionTool
from qdls.kopl.kopl import KoPLEngine

# Define structured types for better schema generation
class EntityTuple(TypedDict):
    ids: Annotated[List[str], "List of entity IDs"]
    triples: Annotated[Optional[List[Dict[str, Any]]], "List of triples containing entity relationships and attributes"]

@dataclass
class KoPLTools:
    """Collection of KoPL API tools for knowledge base operations"""
    
    def __init__(self, engine: KoPLEngine):
        self.engine = engine
        self.tools = self._create_tools()
    
    def _create_tools(self) -> List[FunctionTool]:
        tools = []
        
        # Find tool
        def find(name: str) -> Tuple[List[str], None]:
            """Find all entities with a specific name in the knowledge base
            
            Args:
                name: The name of the entity to search for
            Returns:
                A tuple containing a list of entity IDs and None
            """
            return self.engine.Find(name)
        tools.append(FunctionTool(
            func=find,
            name="Find",
            description="Find all entities with a specific name in the knowledge base"
        ))

        # FindAll tool
        def find_all() -> Tuple[List[str], None]:
            """Returns all entities in the knowledge base
            
            Returns:
                A tuple containing a list of all entity IDs and None
            """
            return self.engine.FindAll()
        tools.append(FunctionTool(
            func=find_all,
            name="FindAll",
            description="Returns all entities in the knowledge base"
        ))

        # FilterConcept tool
        def filter_concept(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            concept_name: Annotated[str, "The name of the concept to filter by"]
        ) -> EntityTuple:
            """Filter entities by a specific concept/type"""
            result = self.engine.FilterConcept(entities, concept_name)
            return {"ids": result[0], "triples": result[1]}
        tools.append(FunctionTool(
            func=filter_concept,
            name="FilterConcept",
            description="Filter entities by a specific concept/type"
        ))

        # FilterStr tool  
        def filter_str(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"], 
            key: str,
            value: str
        ) -> Tuple[List[str], List]:
            """Filter entities by string attribute
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The string attribute key to filter on
                value: The string value to match exactly
            Returns:
                A tuple containing filtered entity IDs and their corresponding attribute triples
            """
            return self.engine.FilterStr(entities, key, value)
        tools.append(FunctionTool(
            func=filter_str,
            name="FilterStr",
            description="Filter entities by string attribute value"
        ))

        # FilterNum tool
        def filter_num(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            key: str,
            value: str,
            op: str
        ) -> Tuple[List[str], List]:
            """Filter entities by numeric attribute value
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The attribute key to filter on
                value: The numeric value to compare against
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                A tuple containing filtered entity IDs and their corresponding attribute triples
            """
            return self.engine.FilterNum(entities, key, value, op)
        tools.append(FunctionTool(
            func=filter_num,
            name="FilterNum",
            description="Filter entities by numeric attribute value"
        ))

        # FilterDate tool
        def filter_date(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            key: str,
            value: str,
            op: str
        ) -> Tuple[List[str], List]:
            """Filter entities by date attribute value
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The date attribute key to filter on
                value: The date value to compare against (YYYY-MM-DD format)
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                A tuple containing filtered entity IDs and their corresponding attribute triples
            """
            return self.engine.FilterDate(entities, key, value, op)
        tools.append(FunctionTool(
            func=filter_date,
            name="FilterDate",
            description="Filter entities by date attribute value"
        ))

        # FilterYear tool
        def filter_year(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            key: str,
            value: str,
            op: str
        ) -> Tuple[List[str], List]:
            """Filter entities by year attribute value
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The year attribute key to filter on
                value: The year value to compare against (YYYY format)
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                A tuple containing filtered entity IDs and their corresponding attribute triples
            """
            return self.engine.FilterYear(entities, key, value, op)
        tools.append(FunctionTool(
            func=filter_year,
            name="FilterYear",
            description="Filter entities by year attribute value"
        ))

        # QFilterStr tool
        def q_filter_str(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            qkey: str,
            qvalue: str
        ) -> Tuple[List[str], List]:
            """Filter entities by string qualifier value
            
            Args:
                entities: A tuple containing entity IDs and triple list
                qkey: The qualifier key to filter on
                qvalue: The string value to match exactly
            Returns:
                A tuple containing filtered entity IDs and their corresponding triples
            """
            return self.engine.QFilterStr(entities, qkey, qvalue)
        tools.append(FunctionTool(
            func=q_filter_str,
            name="QFilterStr",
            description="Filter entities by string qualifier value"
        ))

        # QFilterNum tool
        def q_filter_num(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            qkey: str,
            qvalue: str,
            op: str
        ) -> Tuple[List[str], List]:
            """Filter entities by numeric qualifier value
            
            Args:
                entities: A tuple containing entity IDs and triple list
                qkey: The qualifier key to filter on
                qvalue: The numeric value to compare against
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                A tuple containing filtered entity IDs and their corresponding triples
            """
            return self.engine.QFilterNum(entities, qkey, qvalue, op)
        tools.append(FunctionTool(
            func=q_filter_num,
            name="QFilterNum",
            description="Filter entities by numeric qualifier value"
        ))

        # QFilterDate tool
        def q_filter_date(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            qkey: str,
            qvalue: str,
            op: str
        ) -> Tuple[List[str], List]:
            """Filter entities by date qualifier value
            
            Args:
                entities: A tuple containing entity IDs and triple list
                qkey: The qualifier key to filter on
                qvalue: The date value to compare against (YYYY-MM-DD format)
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                A tuple containing filtered entity IDs and their corresponding triples
            """
            return self.engine.QFilterDate(entities, qkey, qvalue, op)
        tools.append(FunctionTool(
            func=q_filter_date,
            name="QFilterDate",
            description="Filter entities by date qualifier value"
        ))

        # QFilterYear tool
        def q_filter_year(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            qkey: str,
            qvalue: str,
            op: str
        ) -> Tuple[List[str], List]:
            """Filter entities by year qualifier value
            
            Args:
                entities: A tuple containing entity IDs and triple list
                qkey: The qualifier key to filter on
                qvalue: The year value to compare against (YYYY format)
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                A tuple containing filtered entity IDs and their corresponding triples
            """
            return self.engine.QFilterYear(entities, qkey, qvalue, op)
        tools.append(FunctionTool(
            func=q_filter_year,
            name="QFilterYear",
            description="Filter entities by year qualifier value"
        ))

        # QueryAttr tool
        def query_attr(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            key: str
        ) -> List[Any]:
            """Query attribute values for given entities
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The attribute key to query
            Returns:
                A list of attribute values
            """
            return self.engine.QueryAttr(entities, key)
        tools.append(FunctionTool(
            func=query_attr,
            name="QueryAttr",
            description="Query attribute values for given entities"
        ))

        # QueryAttrQualifier tool
        def query_attr_qualifier(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            key: str,
            value: str,
            qkey: str
        ) -> List[Any]:
            """Query qualifier values for specific attribute values
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The attribute key
                value: The attribute value
                qkey: The qualifier key to query
            Returns:
                A list of qualifier values
            """
            return self.engine.QueryAttrQualifier(entities, key, value, qkey)
        tools.append(FunctionTool(
            func=query_attr_qualifier,
            name="QueryAttrQualifier",
            description="Query qualifier values for specific attribute values"
        ))

        # QueryAttrUnderCondition tool
        def query_attr_under_condition(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            key: str,
            qkey: str,
            qvalue: str
        ) -> List[Any]:
            """Query attribute values under specific qualifier conditions
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The attribute key to query
                qkey: The qualifier key condition
                qvalue: The qualifier value condition
            Returns:
                A list of attribute values meeting the qualifier conditions
            """
            return self.engine.QueryAttrUnderCondition(entities, key, qkey, qvalue)
        tools.append(FunctionTool(
            func=query_attr_under_condition,
            name="QueryAttrUnderCondition",
            description="Query attribute values under specific qualifier conditions"
        ))

        # QueryRelation tool
        def query_relation(
            s_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            t_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"]
        ) -> List[str]:
            """Query relations between two sets of entities
            
            Args:
                s_entities: Source entities tuple
                t_entities: Target entities tuple
            Returns:
                A list of relation names between the entities
            """
            return self.engine.QueryRelation(s_entities, t_entities)
        tools.append(FunctionTool(
            func=query_relation,
            name="QueryRelation",
            description="Query relations between two sets of entities"
        ))

        # QueryRelationQualifier tool
        def query_relation_qualifier(
            s_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            t_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            relation: str,
            qkey: str
        ) -> List[Any]:
            """Query qualifier values for specific relations
            
            Args:
                s_entities: Source entities tuple
                t_entities: Target entities tuple
                relation: The relation name
                qkey: The qualifier key to query
            Returns:
                A list of qualifier values
            """
            return self.engine.QueryRelationQualifier(s_entities, t_entities, relation, qkey)
        tools.append(FunctionTool(
            func=query_relation_qualifier,
            name="QueryRelationQualifier",
            description="Query qualifier values for specific relations"
        ))

        # Relate tool
        def relate(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            relation: str,
            direction: str
        ) -> Tuple[List[str], List]:
            """Find entities related to input entities by a specific relation
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                relation: The relation name
                direction: Direction of relation ('forward' or 'backward')
            Returns:
                A tuple containing related entity IDs and their relation triples
            """
            return self.engine.Relate(entities, relation, direction)
        tools.append(FunctionTool(
            func=relate,
            name="Relate",
            description="Find entities related to input entities by a specific relation"
        ))

        # SelectAmong tool
        def select_among(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            key: str,
            op: str
        ) -> List[str]:
            """Select entities with largest/smallest attribute values
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
                key: The numeric attribute key to compare
                op: Selection type ('largest' or 'smallest')
            Returns:
                A list of entity names with extreme attribute values
            """
            return self.engine.SelectAmong(entities, key, op)
        tools.append(FunctionTool(
            func=select_among,
            name="SelectAmong",
            description="Select entities with largest/smallest attribute values"
        ))

        # SelectBetween tool
        def select_between(
            l_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            r_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"], 
            key: str,
            op: str
        ) -> str:
            """Select between two entities based on numeric attribute comparison
            
            Args:
                l_entities: First tuple of entity IDs and optional triples
                r_entities: Second tuple of entity IDs and optional triples
                key: The attribute key to compare
                op: Either 'less' or 'greater'
            Returns:
                Name of the entity meeting the comparison criterion
            """
            return self.engine.SelectBetween(l_entities, r_entities, key, op)
        tools.append(FunctionTool(
            func=select_between,
            name="SelectBetween",
            description="Compare two entities based on numeric attribute and select one"
        ))

        # And tool
        def and_op(
            l_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            r_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"]
        ) -> Tuple[List[str], None]:
            """Returns the intersection of two entity sets
            
            Args:
                l_entities: First tuple of entity IDs and None/triple list
                r_entities: Second tuple of entity IDs and None/triple list
            Returns:
                A tuple containing the intersection of entity IDs and None
            """
            return self.engine.And(l_entities, r_entities)
        tools.append(FunctionTool(
            func=and_op,
            name="And",
            description="Get the intersection of two entity sets"
        ))

        # Or tool
        def or_op(
            l_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"],
            r_entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"]
        ) -> Tuple[List[str], None]:
            """Returns the union of two entity sets
            
            Args:
                l_entities: First tuple of entity IDs and None/triple list
                r_entities: Second tuple of entity IDs and None/triple list
            Returns:
                A tuple containing the union of entity IDs and None
            """
            return self.engine.Or(l_entities, r_entities)
        tools.append(FunctionTool(
            func=or_op,
            name="Or",
            description="Get the union of two entity sets"
        ))

        # Count tool
        def count(
            entities: Annotated[EntityTuple, "Tuple of entity IDs and their triples"]
        ) -> int:
            """Count the number of entities
            
            Args:
                entities: A tuple containing entity IDs and None/triple list
            Returns:
                The count of entities
            """
            return self.engine.Count(entities)
        tools.append(FunctionTool(
            func=count,
            name="Count",
            description="Count the number of entities"
        ))

        # Verify tools
        def verify_str(
            s_value: List[Any],
            t_value: str
        ) -> str:
            """Verify string attribute values against a target value
            
            Args:
                s_value: List of values to verify
                t_value: Target string value
            Returns:
                'yes', 'no', or 'not sure'
            """
            return self.engine.VerifyStr(s_value, t_value)
        tools.append(FunctionTool(
            func=verify_str,
            name="VerifyStr",
            description="Verify string attribute values against a target value"
        ))

        def verify_num(
            s_value: List[Any],
            t_value: str,
            op: str
        ) -> str:
            """Verify numeric attribute values against a target value
            
            Args:
                s_value: List of values to verify
                t_value: Target numeric value
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                'yes', 'no', or 'not sure'
            """
            return self.engine.VerifyNum(s_value, t_value, op)
        tools.append(FunctionTool(
            func=verify_num,
            name="VerifyNum",
            description="Verify numeric attribute values against a target value"
        ))

        def verify_date(
            s_value: List[Any],
            t_value: str,
            op: str
        ) -> str:
            """Verify date attribute values against a target value
            
            Args:
                s_value: List of values to verify
                t_value: Target date value (YYYY-MM-DD format)
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                'yes', 'no', or 'not sure'
            """
            return self.engine.VerifyDate(s_value, t_value, op)
        tools.append(FunctionTool(
            func=verify_date,
            name="VerifyDate",
            description="Verify date attribute values against a target value"
        ))

        def verify_year(
            s_value: List[Any],
            t_value: str,
            op: str
        ) -> str:
            """Verify year attribute values against a target value
            
            Args:
                s_value: List of values to verify
                t_value: Target year value (YYYY format)
                op: Comparison operator ('=', '!=', '<', or '>')
            Returns:
                'yes', 'no', or 'not sure'
            """
            return self.engine.VerifyYear(s_value, t_value, op)
        tools.append(FunctionTool(
            func=verify_year,
            name="VerifyYear",
            description="Verify year attribute values against a target value"
        ))

        return tools
    

if __name__ == '__main__':
    from qdls.utils import print_dict
    tools = KoPLTools(None)
    for t in tools.tools:
        if t.schema['name'] == 'FilterConcept':
            print_dict(t.schema)
            print()
    
