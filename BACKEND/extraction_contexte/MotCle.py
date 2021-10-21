import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords") 
stop_words = set(stopwords.words('english')) 
class MotCle:
    def préparer_data(cleaned):
        cleaned=cleaned.replace('\n','')
        cleaned=cleaned.lower()
        sentences=cleaned.split(".")
        CleanSents=""
        FinalText=""
#removing characters that are not letters 
        for s in sentences :
            s1=re.sub('[\W_]+',' ',s)
            s1=re.sub('[\d_]+',' ',s1)
            CleanSents+=s1+"."

#removing stop words
        words=CleanSents.split()
        for w in words :
            if w in stop_words:
                words.remove(w)
            else :
                FinalText+=w+" "
        dataset=FinalText.split(".")
        return dataset
    def TF_IDF(dataset):
        #This is to Transform a count matrix to a normalized tf-idf representation
        tfIdfTransformer = TfidfTransformer(use_idf=True)
        #This is to Convert a collection of text documents to a matrix of token counts
        countVectorizer = CountVectorizer()
        #Learn the vocabulary dictionary and return document-term matrix
        wordCount = countVectorizer.fit_transform(dataset)
        #Fit to data, then transform it
        newTfIdf = tfIdfTransformer.fit_transform(wordCount)
        #This is for representing the keywords
        df = pd.DataFrame(newTfIdf[0].T.todense(), index=countVectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
        return (list(df['TF-IDF'].head(5).index))
