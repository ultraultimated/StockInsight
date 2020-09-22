from elasticsearch import Elasticsearch
from config import *
import requests
import json

#define elastic instance
es = Elasticsearch(hosts=[{'host': elasticsearch_host, 'port': elasticsearch_port}],
                   http_auth=(elasticsearch_user, elasticsearch_password),maxsize=20)
        
   
def create_index(f,index_name):
    '''
    Function to create index pattern for news and tweets
    INPUT: Json File
    OUTPUT: Creates index in kibana with name "index_name"
    '''
    list_data = json.load(f) 
    j=1
    for data in list_data:
        for k,v in data.items():
            for t in v:
                doc = t
                res = es.index(index=index_name, id=j, ignore=[400,404], body=doc)
                j+=1
                
def create_index_predictions(f,index_name):
    '''
    Function to create index pattern for predictions
    INPUT: Json File
    OUTPUT: Creates index in kibana with name "index_name"
    '''
    list_data = json.load(f) 
    j=1
    for data in list_data:
        doc = data
        res = es.index(index=index_name, id=j, ignore=[400,404], body=doc)
        print(res['result'])
        j+=1
    