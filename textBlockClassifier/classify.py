import pandas as pd

df = pd.read_csv('C:/dev/classification/Mercher.csv',delimiter=';')

# remove redundand columns (some of them are removed temporarily)
df.drop(columns = ['id','text','content_element','url','class_ob','element_id','style','href','color','font-family',
	# those columns probably should be processed in future versions: 
	'presence_of_vendor','presence_of_link','integer','float',
	#'presence_of_ruble','size_width','size_height', # TEMP???
	'presence_of_at','has_point','distance_btw_el_and_ruble','distance_btw_el_and_article','path'], 
	axis = 1, inplace=True) 

#print (df.head(100))
#for ind in df.index:
#     print(df['class'][ind],df['length'][ind],df['enclosure'][ind],df['count'][ind],df['location_x'][ind],
#           df['location_y'][ind],df['n_digits'][ind],df['writing_form'][ind],df['font-size'][ind]);

Y=df['class'] # what to predict
X=df.drop ('class',axis=1) # all other data 
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test  = train_test_split(X, Y, test_size = 0.3, shuffle = True)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

############################################################################
# Linear Regression approach
from base import LinearRegression
LR = LinearRegression() # create model
LR.fit(X_train, Y_train) # train model
Y_LR = LR.predict(X_test) # predict values for test dataset

# show some metrics
print ('LinearRegression metrics:')
print ('MAE:', round (mean_absolute_error(Y_test, Y_LR),3))		
print ('SMSE:', round (mean_squared_error(Y_test, Y_LR)**(1/2),3))
print ('R2_score:', round (r2_score(Y_test, Y_LR),3))

############################################################################
# Decision Tree approach
from tree import DecisionTreeRegressor
TR = DecisionTreeRegressor() # create model
TR.fit(X_train, Y_train) # train model
Y_TR = TR.predict(X_test) # predict values for test dataset

# show some metrics
print ('DecisionTreeRegressor metrics:')
print ('MAE:', round (mean_absolute_error(Y_test, Y_TR),3))		
print ('SMSE:', round (mean_squared_error(Y_test, Y_TR)**(1/2),3))
print ('R2_score:', round (r2_score(Y_test, Y_TR),3))
