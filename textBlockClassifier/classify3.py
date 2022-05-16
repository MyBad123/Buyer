# для качественного обучения важно, чтобы все классы были 
# представлены примерно равномерно (сопоставимое кол-во эл-тов)
#
# на датасете 'Csv_belobuv_new_part.csv' хорошо показали себя следующие парметры:
# length, size_height, n_digits, digits_length, 
# где digits_length — соотношение кол-ва цифр к общему кол-ву символов
#
# за основу взят classify2.py, из которого удален параметр size_height, 
# добавлены генерируемые параметры: 
#   is_price   - в поле text есть признаки цены (рез-т ф-ции is_price);
#   h1_or_href - в поле id eсть тэги <h1> или <a href>

import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import numpy as np
import pickle 
import sys
import os
import re 

def get_n_words(text):
  if not isinstance(text, str) or len(text)==0:
    return 0
  words = text.split()
  return len(words)

def is_article(entry):
  if not isinstance(entry, str) or len(entry)==0:
    return 0
  if re.fullmatch('Артикул[\s]?:.*',entry,flags=re.IGNORECASE):
    return 1
  if re.fullmatch('Арт\.[:]?.*',entry,flags=re.IGNORECASE):
    return 1
  if re.fullmatch('Артикул\s.*',entry,flags=re.IGNORECASE):
    return 1
  return 0

def is_price(entry):
  #print ('is_price(',entry,')');
  if not isinstance(entry, str) or len(entry)==0:
    return 0
  if re.fullmatch('[\d\., ]+$',entry):
    return 1
  if re.fullmatch('[\d\., ]+₽',entry):
    return 1
  if re.fullmatch('[\d\., ]+р\.?',entry,flags=re.IGNORECASE):
    return 1
  if re.fullmatch('[\d\., ]+руб\.?',entry,flags=re.IGNORECASE):
    return 1
  return 0
              
def is_h1_or_href(entry):
  if not isinstance(entry, str) or len(entry)==0:
    return 0
  if re.fullmatch('a\/\/.*',entry,flags=re.IGNORECASE):
    return 1
  if re.fullmatch('h1\/\/.*',entry,flags=re.IGNORECASE):
    return 1
  if re.fullmatch('title\/\/.*',entry,flags=re.IGNORECASE):
    return 1
  return 0

if len(sys.argv) != 3:
  print ('Usage: python classify2.py {csv file} train|predict')
  quit()

if sys.argv[2] != 'train' and sys.argv[2] != 'predict':
  print ('Invalid 2nd parameter: it must be "train" or "predict"')
  quit()

old_df = pd.read_csv(str(sys.argv[1]),delimiter=',')
print ('Reading dataset',sys.argv[1])

# calculate additional ML parameters
old_df['is_article'] = [is_article(x) for x in old_df['text']]
old_df['is_price'] = [is_price(x) for x in old_df['text']]
old_df['h1_or_href'] = [is_h1_or_href(x) for x in old_df['id_xpath']]
old_df['n_words'] = [get_n_words(x) for x in old_df['text']]

# filter columns
df = old_df.filter(['class','length','n_digits','presence_of_at','is_price','h1_or_href','is_article'], axis=1)
#df['digits_length'] = df['n_digits']/df['length']

#df=df[df['class']==3]
#print (df.head(20))

if sys.argv[2] == 'train':
  Y=df['class'] # what to predict
  X=df.drop ('class',axis=1) # all other data 

  from sklearn.model_selection import train_test_split
  X_train, X_test, Y_train, Y_test  = train_test_split(X, Y, test_size = 0.3, shuffle = True)

  SVC_model = SVC()

  # В KNN-модели нужно указать параметр n_neighbors
  # Это число точек, на которое будет смотреть
  # классификатор, чтобы определить, к какому классу принадлежит новая точка
  KNN_model = KNeighborsClassifier(n_neighbors=5)

  SVC_model.fit(X_train, Y_train)
  KNN_model.fit(X_train, Y_train)

  # Now we save the models
  # Its important to use binary mode 
  knnPickle = open(os.path.join(os.path.dirname(__file__),'knn.pkl'), 'wb') 
  svcPickle = open(os.path.join(os.path.dirname(__file__),'svc.pkl'), 'wb') 

  # source, destination 
  pickle.dump(KNN_model, knnPickle) 
  pickle.dump(SVC_model, svcPickle) 

  SVC_prediction = SVC_model.predict(X_test)
  KNN_prediction = KNN_model.predict(X_test)

  # Оценка точности — простейший вариант оценки работы классификатора
  print('SVC accuracy score:',accuracy_score(SVC_prediction, Y_test))
  print('KNN accuracy score:',accuracy_score(KNN_prediction, Y_test))

else: # predict

  KNN_model = pickle.load(open(os.path.join(os.path.dirname(__file__),'knn.pkl'), 'rb'))
  SVC_model = pickle.load(open(os.path.join(os.path.dirname(__file__),'svc.pkl'), 'rb'))

  Y=df['class'] # what to predict
  Y = np.array([int(i) for i in Y])
  X=df.drop ('class',axis=1) # all other data 

  print('Total entries=',len(Y))

  knn_res = KNN_model.predict(X)
  #print('knn_res.len=',len(knn_res))
  svc_res = SVC_model.predict(X)
  #print('svc_res.len=',len(svc_res))

  #print (Y[0:20])
  #print (knn_res[0:20])
  #print (svc_res[0:20])

  # collect common elements of source (Y) and predicted values
  Y_knn = Y[Y==knn_res]
  print('KNN correct predictions=',len(Y_knn))
  Y_svc = Y[Y==svc_res]
  print('SVC correct predictions=',len(Y_svc))

  print('Knn ratio=',100*len(Y_knn)/len(Y),'%')
  print('Svc ratio=',100*len(Y_svc)/len(Y),'%')