
from keras.preprocessing.text import Tokenizer
from nltk.tokenize import word_tokenize,sent_tokenize
import re
import string
import pickle

class AnalyseData:
    def clean_data(doc):
        cleaned = doc.lower()
        #supprimer les retours a la ligne
        cleaned = cleaned.replace("\n", " ")
        punctuation="\"#$%&()*+,-/:;<=>@[\]^_`{|}~"
        for p in cleaned :
            #supprimer  les caractéres indésirables
            if p in punctuation :
                cleaned=cleaned.replace(p, '')
            #supprimer les nombres
            cleaned=cleaned.replace(p,re.sub('[\d_]+','',p))
            #ignorer les caractéres non asci
            encoded_string= p.encode("ascii", "ignore")
            cleaned = cleaned.replace(p,encoded_string.decode())
            
            
        return cleaned

        
    def Construire_sentences(cleaned):
        #charger les phrases deja générées
        with open("./models/sentences.txt", "rb") as fs:   
            sentences = pickle.load(fs)
        for i in sent_tokenize(cleaned):
            temp = []  
            # tokenize the sentence into words et reassembler les mots d'une meme 
            #phrase en une liste
            for j in word_tokenize(i):
                if (j not in string.punctuation):
                    temp.append(j.lower())
            
            sentences.append(temp)
            #enregistrer les nouveaux phrases
        with open("./models/sentences.txt", "wb") as fs:   
            pickle.dump(sentences, fs)
        return sentences
        

    def Construire_sequences(sentences):
        #longeur des sequeces
        train_len = 5
        #charger les sequences déja préparés
        with open("./models/sequences.txt", "rb") as fp:   
            text_sequences = pickle.load(fp)
        #ajouter les nouveaux sequences 
        for sent in sentences:
            for i in range(train_len,len(sent)+1):
                seq = sent[i-train_len:i]
                text_sequences.append(seq)
        #enregistrer les séquences obtenus
        with open("./models/sequences.txt", "wb") as fp:   
            pickle.dump(text_sequences, fp)
        return text_sequences

        
