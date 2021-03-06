# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 17:02:23 2019

@author: Vejay Karthy S
"""

#FINAL




import sys
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras.models import Model
from keras.models import Sequential
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding, GRU, Conv1D, MaxPooling1D, Flatten, SimpleRNN
from keras.optimizers import RMSprop
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras import metrics


# Please change drive location as required
from google.colab import drive
drive.mount('/content/gdrive/')
with open('/content/gdrive/My Drive/SS Lab/Copyofsmoke_features_final11.csv', 'r') as f:
  df = pd.read_csv(f,delimiter=',',encoding='latin-1')
  

sess1 = tf.Session()

df.info()
print(df.shape)
df=df[['Presence_of_Smoke','Area','ROG','Color','Severity1']]



##create input and output vectors
X = df.iloc[:,0:4]
Y = df.iloc[:,4]
print(X.shape)
X = X.values.reshape(1467, 4, 1)
Y = Y.values.reshape(1467, 1)


Z = Y
from keras.utils import to_categorical
Y = to_categorical(Y)
total_rows = 1467 * 4
max_len=4


## splitting of training and testing data
X_train,X_test,Z_train,Z_test = train_test_split(X,Z,test_size=0.20)
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.20)

X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))


# create the model (LSTM)
# For stacked Layer
embedding_vecor_length = 1
model = Sequential()
model.add(LSTM(256, dropout=0.3, return_sequences=True, input_shape=(1,4))) #256
model.add(LSTM(128, dropout=0.3, return_sequences=True)) #128
model.add(LSTM(64, dropout=0.3, return_sequences=True)) #64
model.add(LSTM(32)) #32

'''
(For Single Layer)
model.add(LSTM(128, dropout=0.3, return_sequences=True, input_shape=(1,4))) 
model.add(LSTM(128))
'''



model.add((Dense(3, activation='softmax')))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#checkpoint
filepath="weights.best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

predicted1= model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=100, batch_size=12,callbacks=callbacks_list)

model.summary()
scores1 = model.evaluate(X_test, Y_test, verbose=2)
print("Accuracy: %.2f%%" % (scores1[1]*100))
predicted_classes = model.predict_classes(X_test,verbose=1)
print(predicted_classes.shape)
print(predicted_classes)
probs = model.predict_proba(X_test)

top_k = metrics.top_k_categorical_accuracy(Y_test,probs,k=2)
top_k_array = top_k.eval(session=sess1)
print(top_k_array)
print(top_k)


plt.plot(predicted1.history['acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['LSTM'], loc='lower right')
plt.show()


plt.plot(predicted1.history['val_acc'])
plt.title('model accuracy during validation')#during validation
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['LSTM'], loc='lower right')
plt.show()


plt.plot(predicted1.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['LSTM'], loc='upper right')
plt.show()


plt.plot(predicted1.history['val_loss'])
plt.title('model loss during validation')#during validation
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['LSTM'], loc='upper right')
plt.show()
