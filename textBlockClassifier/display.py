# Tool to display particular rows/columns of the specified dataset
# Usage: python display.py {csv file}

import pandas as pd
import re
import sys

if len(sys.argv) != 2:
  print ('Usage: python display.py {csv file}')
  quit()

df = pd.read_csv(str(sys.argv[1]),delimiter=',')
print ('Reading dataset',sys.argv[1])

#df = pd.read_csv('E:/classify/data/Csv_belobuv_new.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_belobuv_new_part.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_belobuv_new_test.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_esmonde_new.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_kamazik_new.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_mercher_new.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_tangleteezer_new.csv',delimiter=',')
#df = pd.read_csv('E:/classify/data/Csv_techclub_new.csv',delimiter=',')

# remove redundand columns (some of them are removed temporarily)
df.drop(columns = ['nn','id','text','content_element','url','class_ob','element_id','style','href','color','font-family',
	# those columns probably should be processed in future versions: 
	'presence_of_vendor','presence_of_link','integer','float',
	'location_x', 'size_width', 'writing_form', 'enclosure', 'count', 
	'presence_of_ruble','font-size', # TEMP???
	'presence_of_at','has_point','distance_btw_el_and_ruble',
	'distance_btw_el_and_article','path'], 
	axis = 1, inplace=True) 

df=df[df['class']=='описание']

#df.drop(columns = ['class'], axis = 1, inplace=True)

#path='f:/python_modules/navec_hudlit_v1_12B_500K_300d_100q.tar'
#navec = Navec.load(path)

# calculate rate of title and add it into ML dataset
#df['title_rate'] = [get_title_rate(x) for x in df['text']]

pd.options.display.max_rows = 300
print (df.head(300))