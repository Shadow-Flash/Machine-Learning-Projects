# -*- coding: utf-8 -*-
"""Spam Classification

Created by: Varun Gupta
"""

#Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')

#Creating Dataset
dataset = pd.read_csv('spam.csv',encoding='latin-1')
dataset.rename(columns = {'v1':'Spam', 'v2':'Messages'}, inplace = True) 
dataset['Spam'].unique()

#Label Encoder
from sklearn.preprocessing import LabelEncoder 
le = LabelEncoder()
dataset['Spam'] = le.fit_transform(dataset['Spam'])
dataset['Spam'].unique()

print(dataset)

#Removing Unnamed Columns
dataset.drop(['Unnamed: 2','Unnamed: 3','Unnamed: 4'],axis=1)
#Interchange The Columns 
dataset.reindex(['Messages','Spam'],axis=1)

#Cleaning the Messages
import re
corpus = []
for i in range(0,5572):
  text = re.sub('[^a-zA-Z]',' ',dataset['Messages'][i])
  text = text.lower()
  text = text.split()
  ps = PorterStemmer()
  text = [ps.stem(word) for word in text if not word in set(stopwords.words('english'))]
  text = ' '.join(text)
  corpus.append(text)
print(corpus)

#Creating the Bag of Words
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:,0].values
print(X)
print(y)

#Splitting the Train and Test Cases
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.40, random_state = 0)

#Training with Naive Bayes
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

#Predicting Test Cases
y_pred = classifier.predict(X_test)
print("Predicted Texts:")
for count in range(len(y_pred)):
  if(y_pred[count] == y_test[count]):
    print(dataset['Messages'][count])

print("Non-Predicted Texts:")
for count in range(len(y_pred)):
  if(y_pred[count] != y_test[count]):
    print(dataset['Messages'][count])

#Making the Confusion Matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)
