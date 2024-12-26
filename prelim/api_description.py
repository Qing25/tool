description = {
    "tools": [
        {
            "name": "Find",
            "description": "Find all entities with a specific name in the knowledge base",
            "required_parameters": [
                {
                    "name": "name",
                    "type": "STRING",
                    "description": "The name of the entity to search for"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "entities",
                    "description": "A tuple containing a list of entity IDs and None"
                }
            ]
        },
        {
            "name": "FindAll",
            "description": "Returns all entities in the knowledge base",
            "required_parameters": [],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "entities",
                    "description": "A tuple containing a list of all entity IDs and None"
                }
            ]
        },
        {
            "name": "FilterConcept",
            "description": "Filter entities by a specific concept/type",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing a list of entity IDs and None/triple list"
                },
                {
                    "name": "concept_name",
                    "type": "STRING",
                    "description": "The name of the concept to filter by"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and None"
                }
            ]
        },
        {
            "name": "FilterNum",
            "description": "Filter entities by a numeric attribute value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing a list of entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The attribute key to filter on"
                },
                {
                    "name": "value",
                    "type": "STRING",
                    "description": "The numeric value to compare against"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding attribute triples"
                }
            ]
        },
        {
            "name": "And", 
            "description": "Returns the intersection of two entity sets",
            "required_parameters": [
                {
                    "name": "l_entities",
                    "type": "TUPLE",
                    "description": "First tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "r_entities", 
                    "type": "TUPLE",
                    "description": "Second tuple containing entity IDs and None/triple list"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "intersection",
                    "description": "A tuple containing the intersection of entity IDs and None"
                }
            ]
        },
        {
            "name": "Or",
            "description": "Returns the union of two entity sets",
            "required_parameters": [
                {
                    "name": "l_entities",
                    "type": "TUPLE", 
                    "description": "First tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "r_entities",
                    "type": "TUPLE",
                    "description": "Second tuple containing entity IDs and None/triple list"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "union",
                    "description": "A tuple containing the union of entity IDs and None"
                }
            ]
        },
        {
            "name": "Count",
            "description": "Counts the number of entities in a set",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "count",
                    "description": "An integer representing the number of entities"
                }
            ]
        },
        {
            "name": "FilterDate",
            "description": "Filter entities by a date attribute value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The date attribute key to filter on"
                },
                {
                    "name": "value",
                    "type": "STRING",
                    "description": "The date value to compare against (YYYY-MM-DD format)"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding attribute triples"
                }
            ]
        },
        {
            "name": "FilterStr",
            "description": "Filter entities by a string attribute value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The string attribute key to filter on"
                },
                {
                    "name": "value",
                    "type": "STRING",
                    "description": "The string value to match exactly"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding attribute triples"
                }
            ]
        },
        {
            "name": "FilterYear",
            "description": "Filter entities by a year attribute value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The year attribute key to filter on"
                },
                {
                    "name": "value",
                    "type": "STRING",
                    "description": "The year value to compare against (YYYY format)"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding attribute triples"
                }
            ]
        },
        {
            "name": "QFilterDate",
            "description": "Filter entities by a date qualifier value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and triple list"
                },
                {
                    "name": "qkey",
                    "type": "STRING",
                    "description": "The qualifier key to filter on"
                },
                {
                    "name": "qvalue",
                    "type": "STRING", 
                    "description": "The date value to compare against (YYYY-MM-DD format)"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding triples"
                }
            ]
        },
        {
            "name": "QFilterNum",
            "description": "Filter entities by a numeric qualifier value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and triple list"
                },
                {
                    "name": "qkey",
                    "type": "STRING",
                    "description": "The qualifier key to filter on"
                },
                {
                    "name": "qvalue",
                    "type": "STRING",
                    "description": "The numeric value to compare against"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding triples"
                }
            ]
        },
        {
            "name": "QFilterStr",
            "description": "Filter entities by a string qualifier value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and triple list"
                },
                {
                    "name": "qkey",
                    "type": "STRING",
                    "description": "The qualifier key to filter on"
                },
                {
                    "name": "qvalue",
                    "type": "STRING",
                    "description": "The string value to match exactly"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding triples"
                }
            ]
        },
        {
            "name": "QFilterYear",
            "description": "Filter entities by a year qualifier value",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and triple list"
                },
                {
                    "name": "qkey",
                    "type": "STRING",
                    "description": "The qualifier key to filter on"
                },
                {
                    "name": "qvalue",
                    "type": "STRING",
                    "description": "The year value to compare against (YYYY format)"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "filtered_entities",
                    "description": "A tuple containing filtered entity IDs and their corresponding triples"
                }
            ]
        },
        {
            "name": "QueryAttr",
            "description": "Query attribute values for given entities",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The attribute key to query"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "values",
                    "description": "A list of attribute values"
                }
            ]
        },
        {
            "name": "QueryAttrQualifier",
            "description": "Query qualifier values for specific attribute values",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The attribute key"
                },
                {
                    "name": "value",
                    "type": "STRING",
                    "description": "The attribute value"
                },
                {
                    "name": "qkey",
                    "type": "STRING",
                    "description": "The qualifier key to query"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "qualifier_values",
                    "description": "A list of qualifier values"
                }
            ]
        },
        {
            "name": "QueryAttrUnderCondition",
            "description": "Query attribute values under specific qualifier conditions",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The attribute key to query"
                },
                {
                    "name": "qkey",
                    "type": "STRING",
                    "description": "The qualifier key condition"
                },
                {
                    "name": "qvalue",
                    "type": "STRING",
                    "description": "The qualifier value condition"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "values",
                    "description": "A list of attribute values meeting the qualifier conditions"
                }
            ]
        },
        {
            "name": "QueryName",
            "description": "Query names of given entities",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "names",
                    "description": "A list of entity names"
                }
            ]
        },
        {
            "name": "QueryRelation",
            "description": "Query relations between two sets of entities",
            "required_parameters": [
                {
                    "name": "s_entities",
                    "type": "TUPLE",
                    "description": "Source entities tuple"
                },
                {
                    "name": "t_entities",
                    "type": "TUPLE",
                    "description": "Target entities tuple"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "relations",
                    "description": "A list of relation names between the entities"
                }
            ]
        },
        {
            "name": "QueryRelationQualifier",
            "description": "Query qualifier values for specific relations",
            "required_parameters": [
                {
                    "name": "s_entities",
                    "type": "TUPLE",
                    "description": "Source entities tuple"
                },
                {
                    "name": "t_entities",
                    "type": "TUPLE",
                    "description": "Target entities tuple"
                },
                {
                    "name": "relation",
                    "type": "STRING",
                    "description": "The relation name"
                },
                {
                    "name": "qkey",
                    "type": "STRING",
                    "description": "The qualifier key to query"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "qualifier_values",
                    "description": "A list of qualifier values"
                }
            ]
        },
        {
            "name": "Relate",
            "description": "Find entities related to input entities by a specific relation",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "relation",
                    "type": "STRING",
                    "description": "The relation name"
                },
                {
                    "name": "direction",
                    "type": "STRING",
                    "description": "Direction of relation ('forward' or 'backward')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "related_entities",
                    "description": "A tuple containing related entity IDs and their relation triples"
                }
            ]
        },
        {
            "name": "SelectAmong",
            "description": "Select entities with largest/smallest attribute values",
            "required_parameters": [
                {
                    "name": "entities",
                    "type": "TUPLE",
                    "description": "A tuple containing entity IDs and None/triple list"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The numeric attribute key to compare"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Selection type ('largest' or 'smallest')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "selected_names",
                    "description": "A list of entity names with extreme attribute values"
                }
            ]
        },
        {
            "name": "SelectBetween",
            "description": "Select between two entities based on attribute comparison",
            "required_parameters": [
                {
                    "name": "l_entities",
                    "type": "TUPLE",
                    "description": "First entity tuple"
                },
                {
                    "name": "r_entities",
                    "type": "TUPLE",
                    "description": "Second entity tuple"
                },
                {
                    "name": "key",
                    "type": "STRING",
                    "description": "The numeric attribute key to compare"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison type ('less' or 'greater')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "selected_name",
                    "description": "Name of the entity meeting the comparison criterion"
                }
            ]
        },
        {
            "name": "VerifyDate",
            "description": "Verify date attribute values against a target value",
            "required_parameters": [
                {
                    "name": "s_value",
                    "type": "LIST",
                    "description": "List of date values to verify"
                },
                {
                    "name": "t_value",
                    "type": "STRING",
                    "description": "Target date value (YYYY-MM-DD format)"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "result",
                    "description": "Verification result ('yes', 'no', or 'not sure')"
                }
            ]
        },
        {
            "name": "VerifyNum",
            "description": "Verify numeric attribute values against a target value",
            "required_parameters": [
                {
                    "name": "s_value",
                    "type": "LIST",
                    "description": "List of numeric values to verify"
                },
                {
                    "name": "t_value",
                    "type": "STRING",
                    "description": "Target numeric value"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "result",
                    "description": "Verification result ('yes', 'no', or 'not sure')"
                }
            ]
        },
        {
            "name": "VerifyStr",
            "description": "Verify string attribute values against a target value",
            "required_parameters": [
                {
                    "name": "s_value",
                    "type": "LIST",
                    "description": "List of string values to verify"
                },
                {
                    "name": "t_value",
                    "type": "STRING",
                    "description": "Target string value"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "result",
                    "description": "Verification result ('yes', 'no', or 'not sure')"
                }
            ]
        },
        {
            "name": "VerifyYear",
            "description": "Verify year attribute values against a target value",
            "required_parameters": [
                {
                    "name": "s_value",
                    "type": "LIST",
                    "description": "List of year values to verify"
                },
                {
                    "name": "t_value",
                    "type": "STRING",
                    "description": "Target year value (YYYY format)"
                },
                {
                    "name": "op",
                    "type": "STRING",
                    "description": "Comparison operator ('=', '!=', '<', or '>')"
                }
            ],
            "optional_parameters": [],
            "return_data": [
                {
                    "name": "result",
                    "description": "Verification result ('yes', 'no', or 'not sure')"
                }
            ]
        }
    ]
}

if __name__ == '__main__':
    for tool in description['tools']:
        print(tool['name'])
        print(tool['description'])
        print("="*100)
    print(len(description['tools']), "in total.")


    fn_names = ['And', 'Count', 'FilterConcept', 'FilterDate', 'FilterNum', 'FilterStr', 'FilterYear', 'Find', 'FindAll', 'Or', 'QFilterDate', 'QFilterNum', 'QFilterStr', 'QFilterYear', 'QueryAttr', 'QueryAttrQualifier', 'QueryAttrUnderCondition', 'QueryName', 'QueryRelation', 'QueryRelationQualifier', 'Relate', 'SelectAmong', 'SelectBetween', 'VerifyDate', 'VerifyNum', 'VerifyStr', 'VerifyYear']
    print(len(fn_names), "in total.")

