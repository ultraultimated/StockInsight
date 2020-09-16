import json
import pickle

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def publish_prediction(pred, request_id):
	"""
	Send pred to app_messages under prediction key
	"""
	producer.send('app_messages', json.dumps({'request_id': request_id, 'prediction': float(pred)}).encode('utf-8'))
	producer.flush()

def read_messages_count(path, repeat_every):
	"""
	Count the predictions given so far
	(may be used in case of retraining)
	"""
	file_list=list(path.iterdir())
	nfiles = len(file_list)
	if nfiles==0:
		return 0
	else:
		return ((nfiles-1)*repeat_every) + len(file_list[-1].open().readlines())

def append_message(message, path, batch_id):
	"""
	Write log of transactions per batch.
	Each batch of 25 transactions.
	"""
	message_fname = 'messages_{}_.txt'.format(batch_id)
	f=open(path/message_fname, "a")
	f.write("%s\n" % (json.dumps(message)))
	f.close()