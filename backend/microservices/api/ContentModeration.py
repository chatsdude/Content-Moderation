from typing import Optional
from flask import Flask
from flask import request, jsonify
import re
from ArticleScraper import ArticleScraper
import spacy
from AIEngine import AIEngine
from collections import defaultdict
import pathlib
import pickle
import joblib
import bz2file as bz2


class ContentModerationAPI:
    
    def __init__(self):
        self.api = "/api/v1/"
        self.app =  Flask(__name__)
        self.urlRegex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.path = pathlib.Path(__file__).parent.resolve()
        self.app.add_url_rule(self.api + "predict","predict",self.startWorkFlow,methods=["POST"])
        self.app.add_url_rule(self.api + "check","check",self.sayHello,methods=["GET"])
        self.app.before_first_request(self.loadModels)

    def getParams(self,request: Optional[str])-> Optional[str]:
        params = request.json if (request.method == 'POST') else request.args
        return params

    def startWorkFlow(self):
        response = defaultdict(dict)
        #Extract comment
        params = self.getParams(request)
    
        text = params.get('comments','').get('text','')
        #Step 1
        #Check if it is a url or normal text
        #Scrape it accordingly using the articlescrape object
        if text and text.isnumeric()==False and bool(re.match(self.urlRegex,text))==True:
            articleObj = ArticleScraper(text)
            textData = articleObj.scrapeArticle()
            #print(textData)
        #TODO: Store the url and text data in redis cache in order to avoid scraping same site again and again
        elif text and not text.isnumeric():
            textData = text
        else:
            response['error'] = "Invalid text"
            return jsonify(response)

        #Step 2 
        #Clean the text
        cleanedText = self.cleanInputData(textData)
        
        #Step 3
        #Predict using voting classifier model
        output,probabilityMap = AIEngine(cleanedText,self.nlpModel).predictUsingVotingClassifier(self.model)
        

        #Step 4
        #Generate output response data
        response['comments']['text'] = textData
        response['Prediction'] = output
        for key in params.get("requestedAttributes"):
            response[key]['value'] = probabilityMap[key]
            response[key]['type'] = 'PROBABILITY'

        

        return jsonify(response)

    
    def cleanInputData(self,textData:str) -> str:
        text=textData.lower()
        cleaned=re.sub(r'[^a-zA-Z]',' ',text)
        sent=self.nlpModel(cleaned)
        tokens=[text for text in sent if (text.is_stop==False)]
        tokens=[text for text in tokens if (text.is_punct)==False]
        tokens=[text.lemma_ for text in tokens]
        to_string=" ".join(tokens)
        clean=re.sub(r'\s{2}|\s{3}|\s{4}|\s{5}',' ',to_string)
        clean=re.sub(r'\s\w\s',' ',clean)
        clean=re.sub(r'\s(ve)\s|\s(nd)\s|\s(st)\s|\s(th)\s|\s(rd)\s','',clean)
        return clean
    
    def sayHello(self):
        response = {"working":"true"}
        return jsonify(response)

    def loadModels(self):
        print("Calling before any request")
        self.nlpModel = spacy.load("en_core_web_md")
        # pathToModel = str(self.path) + '/' + 'Voting.pkl'
        # self.model = joblib.load(open(pathToModel,'rb'))
        data = bz2.BZ2File("smallModel.pbz2", 'rb')
        self.model = pickle.load(data)
        print("Done loading models.")



if __name__ == "__main__":
    api = ContentModerationAPI()
    api.app.run(host="0.0.0.0", port=8080)
else:
    api = ContentModerationAPI().app
