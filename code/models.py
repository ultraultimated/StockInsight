from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout

def build_model(X_train):
    model=Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(X_train.shape[1],1)))
    model.add(LSTM(50,return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',optimizer='adam')
    return model

    # regressor = Sequential()
    # regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (60, 1)))
    # regressor.add(Dropout(rate = 0.2))

    # ##add 2nd lstm layer
    # regressor.add(LSTM(units = 50, return_sequences = True))
    # regressor.add(Dropout(rate = 0.2))
    # ##add 3rd lstm layer
    # regressor.add(LSTM(units = 50, return_sequences = True))
    # regressor.add(Dropout(rate = 0.2))
    # ##add 4th lstm layer
    # regressor.add(LSTM(units = 50, return_sequences = False))
    # regressor.add(Dropout(rate = 0.2))
    # regressor.add(Dense(units = 1))
    # regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')
    # return regressor
