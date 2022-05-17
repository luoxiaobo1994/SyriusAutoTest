#!/usr/bin/python3

import os
import yaml
import json

current_path = os.path.abspath(os.path.dirname(__file__))
print(current_path)
# print(current_path)

with open(current_path +'./jinglebell_config_new.yaml', 'r',encoding='utf-8') as f:
    temp = yaml.safe_load_all(f)
    print(list(temp))
    # print(temp['basic_name'])
    # print(temp['basic_name']['test_name'])
    # print(temp['basic_name']['selected_name'][0])
