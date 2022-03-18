# Content-Moderation

API for analyzing a comment for hate speech or profanity. 

Sample request:

POST /api/v1/predict

{
    "comments":{
        "text": "hello world"
    },
    "requestedAttributes":{
        "Hate Speech":{},
        "Offensive Language":{},
        "Neutral":{}
    }
}


Sample Response:

{
    "Hate Speech": {
        "type": "PROBABILITY",
        "value": 0.2677352270189811
    },
    "Neutral": {
        "type": "PROBABILITY",
        "value": 0.4922466143281323
    },
    "Offensive Language": {
        "type": "PROBABILITY",
        "value": 0.24001815865288653
    },
    "Prediction": "neither",
    "comments": {
        "text": "hello world"
    }
}

