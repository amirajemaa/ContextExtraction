# from firstapp.apps import PredictionConfig
import json
import markovify
class table_markov:
    def __init__(self,data):
        #charger le dictionnaire déja établi
        tf = open('./models/myDictionary.json', "r")
        self.dict_markov = json.load(tf)
        #générer le table de markov pou le nouveau data
        if(data!= ""):
            self.generateTable(data)
            self.convertFreqIntoProb()
    #générer le table de markov avec fréquence
    def generateTable(self,data,k=3):
        for i in range(1,k+1):
            text_model = markovify.Text(data,state_size=i)
            for key in text_model.chain.model.keys():
                self.dict_markov[' '.join(key)]=text_model.chain.model[key]
    def Cleany (self,x):
        for p in x :
              if p in ['.','?','!'] :
                  x1=x.replace(p, '')  
        return x1
    #eliminer les . , ? et ! contenant dans les clés et valeurs 
    def Cleangenerated(self):   
        t1={}
        for x in self.dict_markov.keys():
          if '.' in x or '?' in x or '!' in x:
            x1=self.Cleany(x)   
            if (x1 in self.dict_markov.keys() ):
              t1[x1] =self.dict_markov[x1].update(self.dict_markov[x])
            else: 
              t1[x1]=self.dict_markov[x]
          else:
            t1[x]=self.dict_markov[x]
        t2={}
        for x,y in t1.items():
            t2[x]={}
            if(type(y)== dict):
              for z in list(y):
                if '.' in z or '?' in z or '!' in z:
                  z1=self.Cleany(z)
                  if (z1 in list(y) ):
                    t2[x][z1] =t1[x][z]+t1[x][z1]
                  else: 
                    t2[x][z1] =t1[x][z]
                else :
                  t2[x]=t1[x]
        self.dict_markov =t2
    
      
    #générer le table de markov avec probabilité  
    def convertFreqIntoProb(self):     
        for kx in self.dict_markov.keys():
            s = float(sum(self.dict_markov[kx].values()))
            for k in self.dict_markov[kx].keys():
                self.dict_markov[kx][k] = self.dict_markov[kx][k]/s
    #enregistrer le tableau
    def eregistrerTable(self):
        tf = open("myDictionary.json", "w")
        json.dump(self.dict_markov,tf)
        tf.close()  
    
    def sample_next(self,ctx,next_prediction,k=3):
        if k>3:
            k=3
        ctx=ctx.split()
        ctx = " ".join(ctx[-k:])
        if self.dict_markov.get(ctx) is None:
            return False #si la chaine à vérifier le mot suivante n'existe pas dans le table
        if (next_prediction not in list(self.dict_markov[ctx].keys())):
            return False #si le mot prédit n'existe pas dans les suivants de la chaine donné
        else:
            if(self.dict_markov[ctx][next_prediction])>= (sum(self.dict_markov[ctx].values())/ len(list(self.dict_markov[ctx].values()))):
                return True #si le mot prédit existe aprés la chaine 
                            #avec une probabilité >= la moynne des probabilités
            else:
                return False # sinon
