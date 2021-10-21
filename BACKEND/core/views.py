from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializer import *
from extraction_contexte.Word2vecModel import Word2vecModel
from extraction_contexte.LstmModel import LstmModel
from extraction_contexte.table_markov import table_markov
from types import new_class
from extraction_contexte.Analyser_data import AnalyseData
from extraction_contexte.MotCle import MotCle
import sklearn
import sklearn.externals 
import joblib
import json
import nltk
from nltk.corpus import stopwords 
import tensorflow
from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import re
import string
nltk.download("stopwords") 
stop_words = set(stopwords.words('english')) 
# Create your views here.
  
class ReactView(APIView):
    
    serializer_class = ReactSerializer
    
    def get(self, request):
        print("get")
        detail = [ {"texte": detail.texte,"contexte": detail.contexte} 
        for detail in React.objects.all()]
        d={}
        d['texte']=detail[len(detail)-1]['texte']
        d['contexte']=self.predictContexte(d['texte'])
        return Response(d)
  
    def post(self, request):
        
        longueur=0
        fichier=""
        print(request.data)
        if (request.data['texte']==""):
            with open("./models/new_contexte.txt", "a") as fs: 
                fs.write(request.data['contexte'])
                fs.write("\n")
                fs.close()
            with open("./models/new_contexte.txt", "r") as fs:    
                fichier = fs.read()
                longueur=len(fichier)
                fs.close()
            print("done")
            if(longueur>20):
                self.entrainer(fichier)
                with open("./models/new_contexte.txt", "w") as fs:
                    fs.write("")
                    fs.close()
            
        else:
            d={}
            d['texte']=request.data['texte']
            #d['contexte']=self.predictContexte(d['texte'])
            d['contexte']=""
            serializer = ReactSerializer(data=d)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
               
                return  Response(serializer.data)
    def predictContexte(self ,texte):
   
        doc=MotCle.préparer_data(texte)
        list = MotCle.TF_IDF(doc)
        model_markov = table_markov("")
        word2vec = Word2vecModel([])
        list1=[]
        for mot in list:
            if mot in word2vec.word2vecModel.wv.vocab:
                list1.append(mot)
        model_lstm = keras.models.load_model('./models/model.h5')
        text=""
        pred_word=""
        x=0
        for word in list1 :
            print(word)
            if(word in model_markov.dict_markov["___BEGIN__"].keys() and model_markov.dict_markov["___BEGIN__"][word]>x):
                x = model_markov.dict_markov["___BEGIN__"][word]
                pred_word =  word
        print("first word suggestion:",pred_word)
        text = pred_word
        list1.remove(pred_word)
        word_idxs=[]
        word_idxs.append(word2vec.word2idx(pred_word))
        list_idx=[word2vec.word2idx(word) for word in list1]
        x=[]
        while (len(list_idx)>0) :
            pad_encoded = pad_sequences( [word_idxs], maxlen=4)
            l=[]
            for i in (model_lstm.predict(pad_encoded)[0]).argsort()[::-1]:
                if (i in list_idx):
                    # # or (word2vec.idx2word(i) in stop_words and pred_word not in stop_words ) ):
                    if (word2vec.idx2word(i) in stop_words ):
                        if(i in x):
                            continue
                        pred_word = word2vec.idx2word(i)
                        text+=" "+pred_word
                        word_idxs=word_idxs[1:]
                        word_idxs.append(i)
                        x.append(i)
                        break
                    l.append(i)     
                    if ( model_markov.sample_next(text,word2vec.idx2word(i),k=len(text))) :
                        pred_word = word2vec.idx2word(i)
                        text+=" "+pred_word
                        print(text)
                        list_idx.remove(i)
                        word_idxs=word_idxs[1:]
                        word_idxs.append(i)
                        break
                if (len(l)==len(list_idx)):
                    pred_word = word2vec.idx2word(l[0])
                    text+=" "+pred_word
                    print(text)
                    list_idx.remove(l[0])
                    word_idxs=word_idxs[1:]
                    word_idxs.append(i)
                    break
        return text
    def entrainer(sel,doc):
        
        cleaned = AnalyseData.clean_data(doc)
        print("step1")
        sentences= AnalyseData.Construire_sentences(AnalyseData.clean_data(doc))
        print("step2")
        text_sequence = AnalyseData.Construire_sequences(sentences)
        print("step3")
        word2vec = Word2vecModel(sentences)
        word2vec.enregistrer_modele()
        print("step4")
        modellstm= LstmModel(word2vec.pretrained_weights,word2vec.vocab_size ,word2vec.emdedding_size )
        modellstm.entrainerModel(word2vec.train_data(text_sequence)[0],word2vec.train_data(text_sequence)[1])
        print("step5")
        model_markov = table_markov(cleaned)
        print("step6")
        model_markov.eregistrerTable()       
        print( model_markov.dict_markov.keys() )
        