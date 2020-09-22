import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


## Here we have consider last N days as training data for today's predict values
## X=[[1,......,100],[2,.....,101]]  
## Y=[      101st day,          102     ]
def previous_data(data,prev_days):
    """
    Return: numpy array of train and test set
    ----------------------
    Parameters:
    data: numpy array of train data
    prev_days: number of previos days to consier for prediction
    """
    X,Y=[],[]
    
    for i in range(len(data)-prev_days-1):
        previous=data[i:i+prev_days,0]
        X.append(previous)
        Y.append(data[i+prev_days,0])
        
    return np.array(X),np.array(Y)

def read_data(filename):
    """
    Return: pandas dataframe
    ---------------------
    Parameters:
    filename: csv file to read
    """
    df = pd.read_csv(filename)
    return df


def transform_data(filename1, filename2):
    """
    Return: train and test set in format required by LSTM model
    --------------------
    Parameters: 
    filename1: train_data filename
    filename2: test_data filename
    """
    df_train = read_data(filename1)
    df_test = read_data(filename2)

    # Normalizing the dataset in range 0,1
    scaler = MinMaxScaler(feature_range=(0,1))
    df_train_close = df_train['close']
    df_train_close = scaler.fit_transform(np.array(df_train_close).reshape(-1,1))

    df_test_close = df_test['close']
    df_test_close = scaler.fit_transform(np.array(df_test_close).reshape(-1,1))

    X_train,Y_train = previous_data(df_train_close,300)
    X_test,Y_test = previous_data(df_test_close,300)

    ## Reshaping data for LSTM
    X_train = X_train.reshape(X_train.shape[0],X_train.shape[1],1)
    X_test = X_test.reshape(X_test.shape[0],X_test.shape[1],1)

    return (X_train, X_test, Y_train, Y_test)

