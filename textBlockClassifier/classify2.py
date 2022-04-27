# для качественного обучения важно, чтобы все классы были 
# представлены примерно равномерно (сопоставимое кол-во эл-тов)
#
# на датасете 'Csv_belobuv_new_part.csv' хорошо показали себя следующие парметры:
# length, size_height, n_digits, digits_length, 
# где digits_length — соотношение кол-ва цифр к общему кол-ву символов

import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import pickle 
import sys
import os

if len(sys.argv) != 3:
  print ('Usage: python classify2.py {csv file} train|predict')
  quit()

if sys.argv[2] != 'train' and sys.argv[2] != 'predict':
  print ('Invalid 2nd parameter: it must be "train" or "predict"')
  quit()

df = pd.read_csv(str(sys.argv[1]),delimiter=',')
print ('Reading dataset',sys.argv[1])

#df = pd.read_csv('E:/classify/data/out.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_belobuv_new_part.csv',delimiter=',')

# load combined dataset Csv_belobuv_new_part + Csv_esmonde_new_part
#df = pd.read_csv('E:/classify/data/Csv_belobuv_new_part_Csv_esmonde_new_part.csv',
#	delimiter=',')

# TODO: calculate additional ML parameters
# df['title_rate'] = [len(x) for x in df['text']]
df['digits_length'] = df['n_digits']/df['length']

# remove redundand columns (some of them are removed temporarily)
#df.drop(columns = ['nn','id','text','content_element','url','class_ob',
#	'element_id','style','href','color','font-family',
#	# those columns probably should be processed in future versions: 
#	'presence_of_vendor','presence_of_link','integer','float',
#	'presence_of_ruble', 'location_x', 'location_y',
#        'size_width','size_height', # TEMP???
#	'distance_btw_el_and_ruble',
#	'presence_of_at','has_point','distance_btw_el_and_article','path'], 
#	axis = 1, inplace=True) 

df.drop(columns = ['nn','id','text','content_element','url','class_ob','element_id','style','href','color','font-family',
	# those columns probably should be processed in future versions: 
	'presence_of_vendor','presence_of_link','integer','float',
	'location_x', 'location_y', 'size_width', 'writing_form', 'enclosure', 'count', 
	'presence_of_ruble','font-size', # TEMP???
	'presence_of_at','has_point','distance_btw_el_and_ruble',
	'distance_btw_el_and_article','path'], 
	axis = 1, inplace=True) 

#df=df[df['class']!='неизвестно']

#result = [len(x) for x in df['text']]
#print (result)

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

  loc_data = [
	# from Csv_belobuv_new_test.csv
	[41,40,6,0.15], #название
	[16,40,4,0.25], #неизвестно
	[7,40,4,0.57],   #цена
	[21,41,2,0.10], #неизвестно
	[2,18,2,1], #неизвестно
	[41,40,6,0.15], #название
	[16,40,4,0.25], #неизвестно
	[250,36,0,0], #описание
	[7,40,4,0.57], #цена

	# from Csv_esmonde_new.csv
	#[26,0,0,0],  	#неизвестно
	#[28,47,4,0.14], #неизвестно
	#[14,47,0,0],    #название      
	#[8,47,4,0.5],	#цена
	#[22,0,0,0],	#неизвестно
	#[10,332,0,0],	#неизвестно                                      
	[27,40,0,0],	#название
	[42,69,2,0.05], #название
	[14,43,8,0.6],	#неизвестно                                      
	[7,20,4,0.6], 	#цена                                    
	[7,23,4,0.6],	#неизвестно                                      
	[10,0,0,0],	#неизвестно
	[4,19,2,0.5], 	#неизвестно                                      
	[9,30,0,0],	#неизвестно                                      
	[26,46,0,0],	#название
	[10,43,6,0.6],	#неизвестно
	[5,20,3,0.6]	#цена

	# from Csv_techclub_new.csv

	# from Csv_whitesecret_new.csv
  ]

  print('KNN:',KNN_model.predict(loc_data))
  print('SVC:',SVC_model.predict(loc_data))
  print('>>>> [1 0 2 0 0 1 0 3 2 1 1 0 2 0 0 0 0 1 0 2]')