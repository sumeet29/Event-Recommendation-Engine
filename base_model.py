import pandas as pd
import datetime
import numpy as np
from sklearn import metrics
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB

df = pd.DataFrame()
train_cols = []
train_Y = pd.DataFrame()


def main():

    df, test_len, train_Y, test_Y = readData()

    # Remove columns with maximum unique values
    df = removecols(df)

    col_names_encode_list = ['user_locale', 'same_city', 'user_joinedAt', 'same_country', 'user_gender', 'admin_friend',
                             'cluster', 'user_community']

    # Encodes non-float labels to new unique interger values
    df = labelEncode(col_names_encode_list, df)

    # Make traing and validation set of data
    train_data = df[1:(len(df) - test_len + 1)]
    test_data = df[(len(train_data)):]

    print "Length of train data: ", len(train_data)
    print "Length of validation data: ", len(test_data)

    # print(train_data)
    # Scaling the values for the parameters
    sl = preprocessing.StandardScaler()
    sl.fit(train_data)
    train_data = sl.transform(train_data)
    sl.fit(test_data)
    test_data = sl.transform(test_data)
    print "Preprocessing done for the data."

    # Running different classifiers on data
    print(' ')
    naiveBayesModel(train_data, test_data, train_Y, test_Y)
    print(' ')
    RandomForestModel(train_data, test_data, train_Y, test_Y)
    print(' ')
    logisticModel(train_data, test_data, train_Y, test_Y)
    print(' ')
    logisticSGDModel(train_data, test_data, train_Y, test_Y)



def labelEncode(col_names, df):
    le = preprocessing.LabelEncoder()
    for col in col_names:
        le.fit(np.array(df[col]))
        df[col] = le.transform(np.array(df[col]))
    return df


def readData():
    # Read the file in panda dataframe
    df = pd.read_csv('data/feature_train.csv')
    df['user_age'] = df['user_age'].fillna(df['user_age'].mean())
    # df = df.drop('interested', 1)
    df = df.drop('not_interested', 1)
    df = df.drop('user', 1)
    df = df.drop('event', 1)
    X, y = df.drop('interested', 1), df['interested']
    # X, y = df.drop('not_interested', 1), df['not_interested']

    # Splitting data into training and validation set
    df, test_df, train_Y, test_Y = train_test_split(X, y, test_size=0.33, random_state=42)
    df = df.append(test_df)
    return df, len(test_df), train_Y, test_Y

# Calculate number of unique values in each columns and
# Dropping the columns with all or maximum unique values
def removecols(df):
    for col in list(df.columns.values):
        # print 'Number of unique values in', col, 'is :', len(df[col].unique())
        if (len(df) * 0.75) <= len(df[col].unique()):
            df = df.drop(col, 1)
    return df


def naiveBayesModel(train_data, test_data, train_Y, test_Y):

    # Build Naive Bayes Model
    model = GaussianNB()
    model.fit(train_data, train_Y)
    # print(model)

    # Make predictions
    predicted = model.predict_proba(test_data)
    # print predicted[0:,1]
    print "Naive Bayes :"
    print 'Log Loss :', metrics.log_loss(test_Y, predicted[0:,1])


def RandomForestModel(train_data, test_data, train_Y, test_Y):

    model = RandomForestClassifier()
    model.fit(train_data, train_Y)
    # print(model)

    # Make predictions
    predicted = model.predict_proba(test_data)
    # print predicted[0:,1]
    print "Random Forest Model :"
    print 'Log Loss :', metrics.log_loss(test_Y, predicted[0:,1])


def logisticModel(train_data, test_data, train_Y, test_Y):

    # fit a logistic regression model to the data
    model = LogisticRegression()

    # Build LR Model with SGD and L2 Regularization
    # print(train_data)
    model.fit(train_data, train_Y)
    # print(model)

    # Make predictions
    predicted = model.predict_proba(test_data)
    # print predicted[0:,1]
    print "Logistic Regression (Vanilla): "
    print 'Log Loss :', metrics.log_loss(test_Y, predicted[0:,1])


def logisticSGDModel(train_data, test_data, train_Y, test_Y):

    # fit a logistic regression model to the data
    model = linear_model.SGDClassifier(alpha=0.00025, loss="log", penalty="l2")

    # Build LR Model with SGD and L2 Regularization
    # print(train_data)
    model.fit(train_data, train_Y)
    # print(model)

    # Make predictions
    predicted = model._predict_proba(test_data)
    # print predicted[0:,1]
    print "Logistic Model with SGD and L2 regularization :"
    print 'Log Loss :', metrics.log_loss(test_Y, predicted[0:,1])


if __name__=="__main__":
    main()