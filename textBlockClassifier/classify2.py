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

#df = pd.read_csv('E:/classify/data/out.csv',delimiter=',')
df = pd.read_csv('E:/classify/data/Csv_belobuv_new_part.csv',delimiter=',')

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

print (df.head(20))

Y=df['class'] # what to predict
X=df.drop ('class',axis=1) # all other data 

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test  = train_test_split(X, Y, test_size = 0.3, shuffle = True)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=27)

#print(X_train)
#print(y_train)

SVC_model = SVC()
# В KNN-модели нужно указать параметр n_neighbors
# Это число точек, на которое будет смотреть
# классификатор, чтобы определить, к какому классу принадлежит новая точка
KNN_model = KNeighborsClassifier(n_neighbors=5)

SVC_model.fit(X_train, Y_train)
KNN_model.fit(X_train, Y_train)

SVC_prediction = SVC_model.predict(X_test)
KNN_prediction = KNN_model.predict(X_test)

# Оценка точности — простейший вариант оценки работы классификатора
print(accuracy_score(SVC_prediction, Y_test))
print(accuracy_score(KNN_prediction, Y_test))

#length,enclosure,count,location_x,location_y,size_width,size_height,n_digits,writing_form,font-size,distance_btw_el_and_ruble
# TEMP: distance_btw_el_and_ruble is not used now because it is not always extracted 

print(SVC_model.predict([
	# from Csv_belobuv_new_test.csv
	[41,40,6,0.15], #название
	[16,40,4,0.25], #неизвестно
	[7,40,4,0.57],   #цена
	[21,41,2,0.10], #неизвестно
	[2,18,2,1], #неизвестно
	[41,40,6,0.15], #название
	[16,40,4,0.25], #неизвестно
	[250,36,0,0], #описание
	[7,40,4,0.57] #цена

	# from Csv_techclub_new.csv
	#[27,12,6,530,537,128,38,7,3,16], #143.40502083260543 -> название
        #[27,12,6,7,3,16], #143.40502083260543 -> название
	#[12,12,6,530,576,128,23,8,0,15], #135.51752654177244 -> цена
        #[12,12,6,8,0,15], #135.51752654177244 -> цена
	#[15,12,11,668,537,128,38,2,2,16],#278.6862034618865 -> название
        #[15,12,11,2,2,16],#278.6862034618865 -> название
	#[15,12,31,668,576,128,23,0,2,15],#262.0 -> неизвестно
        #[15,12,31,0,2,15],#262.0 -> неизвестно
	#[30,11,3,254,995,128,38,6,3,16], #158.02847844613325, -> название
	#[7,12,3,319,1014,51,19,4,2,16],  #211.12318678913505, -> неизвестно
	#[8,11,3,254,1034,128,23,5,0,15], #143.13629868066312, -> цена
	#[8,11,2,392,1034,128,23,5,0,15], #224.0, -> цена
        #[8,11,2,5,0,15], #224.0, -> цена
	#[34,11,1,530,995,128,58,4,3,16], #143.40502083260543, -> название
	#[8,11,1,530,1053,128,22,5,0,15], #139.30183056945089, -> цена
        #[8,11,1,5,0,15], #139.30183056945089, -> цена
	#[28,11,8,668,995,128,38,5,3,16], #,39.0, -> название

	# from Csv_whitesecret_new.csv
	#[17,12,3,46,1498,228,75,0,1,30],   # 75.0 -> Название
	#[5,12,2,46,1573,228,51,3,0,30],    # 0.0 -> unknown
	#[3,13,3,46,1582,50,33,3,0,30],     # 9.0 -> unknown
	#[293,12,2,46,1624,228,187,0,2,14], # 51.0 -> Описание
	#[6,11,11,46,1866,228,50,0,2,18],   # 293.0 -> unknown
	#[13,12,3,0,0,146,27,0,1,18],       # 0 -> unknown
	#[27,12,3,346,1498,228,107,0,1,30]  # 107.0 -> Название
        #[27,12,3,0,1,30]  # 107.0 -> Название
]))