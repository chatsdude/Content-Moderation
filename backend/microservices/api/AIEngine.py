import pickle
import sklearn
import spacy
import pathlib

class AIEngine:

    def __init__(self,sentTokens,nlpModel):
        self.nlpModel = nlpModel
        self.sentTokens = sentTokens
        self.path = pathlib.Path(__file__).parent.resolve()
        self.probabilityOrder = ['Hate Speech','Neutral','Offensive Language']
        self.probabilityMap = dict()


    def predictUsingVotingClassifier(self):
        try:
            pathToModel = str(self.path) + '/' + 'Voting.pkl'
            vcModel = pickle.load(open(pathToModel,'rb'))
            vectors=self.nlpModel(self.sentTokens).vector.reshape(1,-1)
            output = vcModel.predict(vectors)
            probabilities = vcModel.predict_proba(vectors)
            probabilityList = list(probabilities.flatten())
            for prob,key in zip(probabilityList,self.probabilityOrder):
                self.probabilityMap[key] = prob

            return (output.tolist()[0],self.probabilityMap)
        except Exception as e:
            print(e)
            e.print_exc()
