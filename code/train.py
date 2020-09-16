from models import build_model
from preprocess import transform_data
import os
import tensorflow as tf
from keras.callbacks import Callback, ModelCheckpoint, EarlyStopping

DATA_PATH = '../Data/NKE.csv'
TEST_PATH = '../Data/NKE_Test.csv'
MODEL_PATH = '../model/'
X_train, X_test, Y_train, Y_test = transform_data(DATA_PATH, TEST_PATH)


model = build_model(X_train)


callbacks_list = [ModelCheckpoint(filepath='NKE_Model/ctpn.{epoch:03d}.h5',
                                 monitor='val_loss',
                                 verbose=1,
                                 save_best_only=True,
                                 save_weights_only=True),EarlyStopping(monitor='val_loss', patience=2, verbose=0)]


model.fit(X_train,Y_train,validation_data=(X_test,Y_test),epochs=100,batch_size=64,verbose=1,callbacks=callbacks_list)


