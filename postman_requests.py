import requests
import json

def postman_requests():
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
                "runtime.request"
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

    data = json.loads(response.text)

    # Extracting information from each document
    results = []
    for item in data['data']:
        doc = item['document']
        url = doc['url']
        id = doc['id']
        collection_name = doc['collection']['name']
        publisher_name = doc['publisherName']
        method = doc['method']
        results.append({
            'url': url,
            'id': id,
            'collection_name': collection_name,
            'publisher_name': publisher_name,
            'method': method
        })

    # Printing the extracted information
    for result in results:
        print("URL:", result['url'])
        print("ID:", result['id'])
        print("Collection Name:", result['collection_name'])
        print("Publisher Name:", result['publisher_name'])
        print("Method:", result['method'])
        print()
