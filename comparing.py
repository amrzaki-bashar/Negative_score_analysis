
import requests
import json
import statistics
import pandas as pd
from tqdm import tqdm 

search_query_list = []
with open('assets\\top_100_search_archive_15_3_2022.json') as f:
	data = json.load(f)
	for i in data['aggregations']['search_query']['buckets']:
		search_query_list.append(i['key'])
print(search_query_list)
headers = {'Content-Type': 'application/json'}

result = {}
for search_query in search_query_list:
    default = {}
    with open('default\\'+search_query+'.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
        for i in data['data']:
            default[i["id"]] = i["meta"]["score"]

    new_mapping = {}
    with open('new_mapping_no_b_no_1_no_weight\\'+search_query+'.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
        try:
            for i in data['data']:
                new_mapping[i["id"]] = i["meta"]["score"]
        except:
            pass

    #get difference between them both
    difference = {}
    for key,value in default.items():
        if(key in new_mapping.keys()):
            difference[key] = default[key] - new_mapping[key]
    

    
    same_results = len(difference)
    standard_deviation = -1
    mean = -1
    if(same_results>1):
        mean = statistics.mean(difference.values())
        standard_deviation = statistics.stdev(difference.values())
    result[search_query] = {
        "mean":mean,
        "standard_deviation":standard_deviation,
        "number of same results": same_results}

df = pd.DataFrame(result)
df.T.to_csv('result_with_new_mapping_no_b_no_1_no_weight.csv')

print()