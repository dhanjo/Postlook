import json
import requests

def postman_teams():
    url = 'https://www.postman.com/_api/ws/proxy'
    headers = {
        'Host': 'www.postman.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.postman.com/',
        'Content-Type': 'application/json',
        'Content-Length': '326',
        'Connection': 'close'
    }
    Data = {
        "service": "search",
        "method": "POST",
        "path": "/search-all",
        "body": {
            "queryIndices": [
                "apinetwork.team"
            ],
            "queryText": "",
            "size": 25,
            "from": 0,
            "clientTraceId": "86a583d9-5856-44aa-be4b-c31bd879fca2",
            "requestOrigin": "srp",
            "mergeEntities": "true",
            "nonNestedRequests": "true",
            "domain": "public"
        }
    }

    response = requests.post(url, json=Data, headers=headers)


    data_dict = json.loads(response.text)

    results = []
    for item in data_dict['data']:
        doc = item['document']
        id = doc['id']
        name = doc['name']
        desc = doc['description']
        users = doc['users']
        created = doc['createdat']
        results.append({
            'name': name,
            'id': id,
            'description': desc,
            'users': users,
            'created': created
        })

    # Printing the extracted information
    for result in results:
        print("ID:", result['id'])
        print("NAME:", result['name'])
        print("Description:", result['description'])
        print("Users:", result['users'])
        print("Created:", result['created'])
        print()
