from pandas import DataFrame
import csv, sys
import numpy as np
import pandas as pd
from dateutil.parser import parse
from sklearn import preprocessing
from sklearn.decomposition import PCA

na = ['None', ' ', 'NA', '']

def loadTrainingData(path):
   # Columns: user, event, invited, timestamp, interested, not_interested
   training_data = pd.read_csv(path, header=0, na_values=na)
   return training_data

def labelEncode(col_names, df):
    le = preprocessing.LabelEncoder()
    for col in col_names:
        le.fit(np.array(df[col]))
        df[col] = le.transform(np.array(df[col]))
    return df

def 
def main():

   training_data = loadTrainingData('/home/jeevan/Downloads/feature_train.csv')
   col_names_encode_list = ['user_locale', 'same_city', 'user_joinedAt', 'same_country', 'user_gender', 'admin_friend',
                             'cluster', 'user_community']

    # Encodes non-float labels to new unique interger values
   training_data = labelEncode(col_names_encode_list, training_data)

   #pca
   imp = preprocessing.Imputer(missing_values='NaN', strategy='median', axis=1)
   imp.fit(training_data) 
   training_data = DataFrame(imp.fit_transform(training_data))
   
   pca = PCA(n_components=0.9999)
   training_data = pca.fit_transform(training_data)
   print(pca.explained_variance_ratio_)
   print(pca.n_components_)
   print training_data.shape
   

if __name__ == '__main__':
   main()


   
