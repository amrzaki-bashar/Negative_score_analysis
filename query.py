
import requests
import json
from tqdm import tqdm 

search_query_list = []
with open('assets\\top_100_search_archive_15_3_2022.json') as f:
	data = json.load(f)
	for i in data['aggregations']['search_query']['buckets']:
		search_query_list.append(i['key'])
print(search_query_list)
headers = {'Content-Type': 'application/json'}

url = "http://192.168.2.61:5001/jobs/search"

for search_query in tqdm(search_query_list):
	payload = json.dumps({
		"latitude": "0.0",
		"longitude": "0.0",
		"pageSize": 100,
		"query": search_query,
		"searchFilters": {},
		"startIndex": 0
	})
	response = requests.request("POST", url, headers=headers, data=payload)
	default_out = json.loads(response.text)
	with open('default\\'+search_query+'.json', 'w',encoding='utf-8') as outfile:
		json.dump(default_out, outfile, sort_keys = True, indent = 4,ensure_ascii = False)

	payload = json.dumps({
		"latitude": "0.0",
		"longitude": "0.0",
		"pageSize": 100,
		"query": search_query,
		"searchFilters": {},
		"startIndex": 0,
		"index_name":"jobs_no_b_no_1_no_weight"
	})
	response = requests.request("POST", url, headers=headers, data=payload)
	new_mapping_out = json.loads(response.text)
	with open('new_mapping_no_b_no_1_no_weight\\'+search_query+'.json', 'w',encoding='utf-8') as outfile:
		json.dump(new_mapping_out, outfile, sort_keys = True, indent = 4,ensure_ascii = False)

print(response.text)
