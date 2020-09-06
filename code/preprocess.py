import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def transform_data(filename):
    dataset_train = pd.read_csv(filename)
    #keras only takes numpy array
    training_set = dataset_train.iloc[:, 1: 2].values
    sc = MinMaxScaler(feature_range = (0, 1))
    #fit: get min/max of train data
    training_set_scaled = sc.fit_transform(training_set)
    ## 60 timesteps and 1 output
    X_train = []
    y_train = []
    for i in range(2, len(training_set_scaled)):
        X_train.append(training_set_scaled[i-2: i, 0])
        y_train.append(training_set_scaled[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, newshape =  (X_train.shape[0], X_train.shape[1], 1))
    return X_train, y_train
