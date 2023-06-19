import requests
import json

def postman_collections(query):
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
        'service': 'search',
        'method': 'POST',
        'path': '/search-all',
        'body': {
            'queryText': query,
            'from': 0,
            'size': 10,
            'mergeEntities': True,
            'nested': True,
            'clientTraceId': 'c393374b-68ba-490d-b806-5e48e4c4fb2f',
            'requestOrigin': 'dropdown',
            'domain': 'public',
            'queryIndices': ['collaboration.workspace', 'adp.api', 'runtime.collection', 'flow.flow']
        }
    }

    response = requests.post(url, json=Data, headers=headers)
    data_dict = json.loads(response.text)
    output = ""

    for item in data_dict['data']:
        if 'workspaces' in item['document']:
            for workspace in item['document']['workspaces']:
                name = workspace['name']
                workspace_id = workspace['id']
                output += "Workspace Name: " + name + "\n"
                output += "Workspace ID: " + workspace_id + "\n"
        else:
            name = item['document']['name']
            entity_id = item['document']['id']
            publisher_type = item['document']['publisherType']
            publisher_name = item['document']['publisherName']
            output += "\n"
            output += "Entity Name: " + name + "\n"
            output += "Entity ID: " + entity_id + "\n"
            output += "Publisher Type: " + publisher_type + "\n"
            output += "Publisher Name: " + publisher_name + "\n\n"

    return output
