import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Bidirectional
class LstmModel:
  def __init__(self,weights,vocab_size,emdedding_size):
    self.model = Sequential()
    #couche embedding
    self.model.add(Embedding(input_dim=vocab_size, output_dim=emdedding_size, weights=[weights]))
    #couche lstm bidirectionnelles
    self.model.add(Bidirectional(LSTM(units=emdedding_size,return_sequences=True)))
    #2émecouche lstm bidirectionnelles
    self.model.add(Bidirectional(LSTM(units=emdedding_size)))
    #couche dense avec activation relu
    self.model.add(Dense(units=emdedding_size,activation='relu'))
    #couche dense avec activation softmax
    self.model.add(Dense(units=vocab_size, activation='softmax'))
    #compilation
    self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    
  def entrainerModel(self, train_x, train_y):
    #entrainement modele
    self.model.fit(train_x, train_y,batch_size=128,epochs=5)
    #enregistrer modele
    self.model.save('./models/model.h5')