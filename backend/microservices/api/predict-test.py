import requests
import json

requestObj = {
    "comments":{
        "text": "Hello world"
    },
    "requestedAttributes":{
        "Hate Speech":{},
        "Offensive Language":{},
        "Neutral":{}
    }
}

url = 'http://ec2-65-0-105-221.ap-south-1.compute.amazonaws.com:8080/api/v1/predict'
response = requests.post(url, json=requestObj)
result = response.json()

print(json.dumps(result, indent=2))
