# -*- coding: utf-8 -*-
"""
Written by: Vijay Sanjos Alexander
Email: vijaysanjosalexander@gmail.com
Copyright (c) 2017, VSA.
License: MIT (see LICENSE for details)
"""

import json
from py2neo import Node, Relationship, Graph
graph = Graph("http://localhost:7474/db/data/")
graph.delete_all()
parsed_json = json.loads(open('D:/Users/file.json', 'r').read())
# Parser for the Entities in the JSON
for i in parsed_json['entities']:
    # Get the type of the Node (:Person)
    etype=i['type']
    # Creating Node
    entity = Node(etype, name=i['text'], count=i['count'])
    # Will create if not pre-existing
    graph.merge(entity)
    entity.push()
# Array to hold values in Sub-JSON
rel_node = []
rel_type = []
c1 = 0
c = 0
# Parser for the relationship in the JSON
for i in parsed_json['relations']:
    # Relationship name [:MAPS_TO]
    rel_name = i['type']
    # Relationship Attributes
    rel_desc = i['sentence']
    rel_scr = i['score']
    # Get Relationship End points
    for j in i['arguments']:
        rel_node.append(j['text'])
        rel_type.append(j['entities'][0]['type'])
        c1=c1+1
    # Get the start point
    rtype1 = rel_type[c1+c-2]
    # Get the end point
    rtype2 = rel_type[c1+c-1]
    # Create Node for start & end point if not pre-existing
    start = Node(rtype1, name=rel_node[c1+c-2])
    end = Node(rtype2, name=rel_node[c1+c-1])
    graph.merge(start)
    graph.merge(end)
    start.push()
    end.push()
    # Create relationship (N) -[:REL]-> (N)
    relation = Relationship(start, rel_name, end, sentence=rel_desc, score=rel_scr)
    graph.merge(relation)
    relation.push()
# Open browser
graph.open_browser()

