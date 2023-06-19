import json
import requests

def postman_requests(query):
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
    data = {
        "service": "search",
        "method": "POST",
        "path": "/search-all",
        "body": {
            "queryIndices": [
                "runtime.request"
            ],
            "queryText": query,
            "size": 25,
            "from": 0,
            "clientTraceId": "86a583d9-5856-44aa-be4b-c31bd879fca2",
            "requestOrigin": "srp",
            "mergeEntities": "true",
            "nonNestedRequests": "true",
            "domain": "public"
        }
    }

    response = requests.post(url, json=data, headers=headers)
    output = ""

    data_dict = json.loads(response.text)

    results = []
    for item in data_dict['data']:
        doc = item['document']
        url = doc['url']
        id = doc['id']
        collection_name = doc['collection']['name']
        publisher_name = doc['publisherName']
        method = doc.get('method', '')  # Use get() method with a default value to handle missing 'method' key
        results.append({
            'url': url,
            'id': id,
            'collection_name': collection_name,
            'publisher_name': publisher_name,
            'method': method
        })

    # Appending the extracted information to the output
    for result in results:
        output += "URL: " + result['url'] + "\n"
        output += "ID: " + result['id'] + "\n"
        output += "Collection Name: " + result['collection_name'] + "\n"
        output += "Publisher Name: " + result['publisher_name'] + "\n"
        output += "Method: " + result['method'] + "\n\n"

    return output
