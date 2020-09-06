import pdb
import json
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from pathlib import Path
from kafka import KafkaConsumer
from messages_utils import append_message, read_messages_count, send_retrain_message, publish_prediction
from models import build_model
from preprocess import transform_data
from sklearn.preprocessing import MinMaxScaler

KAFKA_HOST = 'localhost:9092'
TOPICS = ['app_messages', 'retrain_topic']
PATH = Path('../')
MODELS_PATH = PATH/'model'
MESSAGES_PATH = PATH/'messages'
RETRAIN_EVERY = 25
EXTRA_MODELS_TO_KEEP = 1

consumer = None
model = None
checkpoint_path = MODELS_PATH/"model_0_.ckpt"

def reload_model(path):
	model = build_model()
	model.load_weights(path)
	return model


def is_retraining_message(msg):
	message = json.loads(msg.value)
	return msg.topic == 'retrain_topic' and 'training_completed' in message and message['training_completed']


def is_application_message(msg):
	message = json.loads(msg.value)
	return msg.topic == 'app_messages' and 'prediction' not in message


def predict(message):
	dataset_test = pd.DataFrame(message, index=[0])
	dataset_train = pd.read_csv('../Data/AAPL.csv')
	dataset_test.columns = dataset_train.columns
	real_stock_price = dataset_test.iloc[:, 1: 2].values
	dataset_total = pd.concat((dataset_train['1. open'],dataset_test['1. open']), axis = 0)
	inputs = dataset_total[len(dataset_total)-len(dataset_test)- 2: ].values
	inputs = inputs.reshape(-1, 1)
	sc = MinMaxScaler(feature_range = (0, 1))
	inputs = sc.fit_transform(inputs)
	inputs = sc.transform(inputs)
	X_test = []
	for i in range(2, len(inputs)):
	    X_test.append(inputs[i-2: i, 0])
	    X_test = np.array(X_test)
	    X_test = np.reshape(X_test, newshape = (X_test.shape[0], X_test.shape[1], 1))
	predicted_stock_price = model.predict(X_test)
	predicted_stock_price = sc.inverse_transform(predicted_stock_price)
	return predicted_stock_price

def start(model_id, messages_count, batch_id):
	for msg in consumer:
		message = json.loads(msg.value)

		if is_retraining_message(msg):
			model_fname = 'model_{}_.p'.format(model_id)
			model = reload_model(MODELS_PATH/model_fname)
			print("NEW MODEL RELOADED {}".format(model_id))

		elif is_application_message(msg):
			request_id = message['request_id']
			pred = predict(message['data'])
			publish_prediction(pred, request_id)

			append_message(message['data'], MESSAGES_PATH, batch_id)
			messages_count += 1
			# if messages_count % RETRAIN_EVERY == 0:
			# 	model_id = (model_id + 1) % (EXTRA_MODELS_TO_KEEP + 1)
			# 	send_retrain_message(model_id, batch_id)
			# 	batch_id += 1


if __name__ == '__main__':

	messages_count = read_messages_count(MESSAGES_PATH, RETRAIN_EVERY)
	batch_id = messages_count % RETRAIN_EVERY

    #model load
	model_id = batch_id % (EXTRA_MODELS_TO_KEEP + 1)
	model_fname = 'model_{}_.ckpt'.format(model_id)
	model = reload_model(MODELS_PATH/model_fname)


	consumer = KafkaConsumer(bootstrap_servers=KAFKA_HOST)
	consumer.subscribe(TOPICS)
	start(model_id, messages_count, batch_id)
