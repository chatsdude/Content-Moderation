
import sklearn
import spacy

class AIEngine:

    def __init__(self,sentTokens,nlpModel):
        self.nlpModel = nlpModel
        self.sentTokens = sentTokens
        self.probabilityOrder = ['Hate Speech','Neutral','Offensive Language']
        self.probabilityMap = dict()


    def predictUsingVotingClassifier(self,model):
        try:
            vectors=self.nlpModel(self.sentTokens).vector.reshape(1,-1)
            output = model.predict(vectors)
            probabilities = model.predict_proba(vectors)
            probabilityList = list(probabilities.flatten())
            for prob,key in zip(probabilityList,self.probabilityOrder):
                self.probabilityMap[key] = prob

            return (output.tolist()[0],self.probabilityMap)
        except Exception as e:
            print(e)
            e.print_exc()
