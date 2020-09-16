import pdb
import json
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from pathlib import Path
from kafka import KafkaConsumer
from sklearn.preprocessing import MinMaxScaler
from messages_utils import append_message, read_messages_count, publish_prediction
from models import build_model
from preprocess import transform_data
from preprocess import read_data
from keras.models import model_from_json

KAFKA_HOST = 'localhost:9092'
TOPICS = ['app_messages', 'retrain_topic']
PATH = Path('../')
MODELS_PATH = PATH/'model/LSTM'
MESSAGES_PATH = PATH/'messages'
RETRAIN_EVERY = 25
EXTRA_MODELS_TO_KEEP = 1
TRAIN_DATA = PATH/'Data/NKE.csv'
consumer = None
model = None


def reload_model(path):
	"""Return TensorFlow model
	loads a model from given path
	"""
	json_file = open(path, 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	
	# load weights into new model
	loaded_model.load_weights(MODELS_PATH/"model.h5")
	print("Loaded model from disk")
	
	loaded_model.compile(loss='mean_squared_error',optimizer='adam')
	return loaded_model


def is_application_message(msg):
	"""
	Returns true : if message arrived at app_messages topic
			false: otherwise
	"""
	message = json.loads(msg.value)
	return msg.topic == 'app_messages' and 'prediction' not in message


def predict(model, message):
	"""Return prediction: float
	Returns closing stock price for given row
	"""
	train_df = read_data(TRAIN_DATA)
	dataset_test = pd.DataFrame(message, index=[0])
	dataset_test.columns = train_df.columns
	scaler = MinMaxScaler(feature_range=(0,1))
	
	df = train_df.tail(300)

	# print('-----------------', df.tail(1))
	df_close = df['close']
	# print(df_close.head())
	# print(df_close.shape)
	df_close = scaler.fit_transform(np.array(df_close).reshape(-1,1))
	X_test = np.array(df_close[len(df_close)-300:, 0])
	temp_list = np.array(X_test).reshape(1,300)
	# print(temp_list.shape)
	# # print(X_test.shape)
	# print('\n')
	# print('----------')
	X_test = X_test.reshape(temp_list.shape[0], temp_list.shape[1], 1)
	predicted_stock_price = model.predict(X_test)
	predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
	train_df = train_df.append(dataset_test, ignore_index=True)
	train_df.to_csv(TRAIN_DATA, index=False)
	return predicted_stock_price


def start(model, messages_count, batch_id):
	"""
	continuously listen to kafka server
	"""
	for msg in consumer:
		message = json.loads(msg.value)

		if is_application_message(msg):
			request_id = message['request_id']
			pred = predict(model, message['data'])
			publish_prediction(pred, request_id)

			append_message(message['data'], MESSAGES_PATH, batch_id)
			messages_count += 1


if __name__ == '__main__':

	messages_count = read_messages_count(MESSAGES_PATH, RETRAIN_EVERY)
	batch_id = messages_count % RETRAIN_EVERY

    #model load
	model_fname = 'model_NKE.json'
	model = reload_model(MODELS_PATH/model_fname)


	consumer = KafkaConsumer(bootstrap_servers=KAFKA_HOST)
	consumer.subscribe(TOPICS)
	start(model, messages_count, batch_id)
