import gensim
import numpy as np
import joblib
class Word2vecModel:
   

    def __init__(self,text_sequences):
        if (text_sequences == []):
            #charger un modele deja entrainé
            self.word2vecModel  =joblib.load('./models/word_model.pkl')
        else:
            #entrainer le modele
            print("word2vec")
            self.word2vecModel = gensim.models.Word2Vec(text_sequences, size=100, min_count=1, window=5, iter=4)
            self.pretrained_weights = self.word2vecModel.wv.vectors
            self.vocab_size, self.emdedding_size = self.pretrained_weights.shape
    #convertir word to index
    def word2idx(self,word):
        return self.word2vecModel.wv.vocab[word].index
    #convertir index to word
    def idx2word(self,idx):
        return   self.word2vecModel.wv.index2word[idx]
    #préparer le train data du lstm
    def train_data(self,text_sequences):
        #initialiser data en entrée
        train_x = np.zeros([len(text_sequences), 5], dtype=np.int32)
        #initialiser data cible
        train_y = np.zeros([len(text_sequences)], dtype=np.int32)
        #remplir le train data par les indices
        for i, sentence in enumerate(text_sequences):
            for t, word in enumerate(sentence[:-1]):
                train_x[i][t] = self.word2idx(word)  
            train_y[i] = self.word2idx(sentence[-1])
        return (train_x,train_y)
    #enregistrer modele
    def enregistrer_modele(self):
        self.word2vecModel.save("./models/word2vec.model")
    
    