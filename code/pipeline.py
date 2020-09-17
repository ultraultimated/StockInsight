#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import json
import re
import time

import en_core_web_lg
import nltk
import numpy as np
import requests
import spacy
import tweepy
from config import *
from elasticsearch import Elasticsearch
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from tweepy import API, Stream, OAuthHandler, TweepError

nlp = en_core_web_lg.load()
from nltk.corpus import stopwords
import datetime
import elk


# Setup twitter Authentication using tweepy
# Arguments can be taken from config file
def authenticate_tweepy():
    """
    Authenticates the twitter using various tokens and keys
    INPUT: get input from config.py file
    OUTPUT: returns the api object which can be used to query twitter
    """
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    return api


# Using yahoo API to fetch latest news from the US stock markets
# use config file to populate x_rapidapi_key
def fetch_yahoo_news(ticker_name_input):
    """
    This Function fetches the stock news from yahoo API
    INPUT: Name of the ticker for which news is required
    OUTPUT: Json list of all news
    """
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-news"

    querystring = {"region": "US", "category": ticker_name_input}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': x_rapidapi_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    resp = response.json()
    return resp


# News of last 24 hours in operation
def filter_yahoo_news(filter_time, ticker_name):
    """
    Filters the news based on time
    INPUT: time in seconds before which the news are relevant and symbol of ticker/stock
    OUTPUT: returns list of news headline and news summary
    """
    resp = fetch_yahoo_news(ticker_name)
    time_consider = time.time() - filter_time  # time in seconds
    sentences_news = []

    list_news = resp["items"]["result"]
    for item in list_news:
        if item["published_at"] > time_consider:
            sentences_news.append(item["title"])
            sentences_news.append(item["summary"])
    return sentences_news


def sentiment_score(sentence, row):
    """
    Function computes sentiment of a sentence and appends the sentiment to the final dictionary which will be used as json to store data.
    INPUT: sentence whose sentiment is to be analyzed and the cureent object which stores other details
    OUTPUT: returns the updated dictionary with sentiment score
    """
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(sentence)

    if scores['compound'] <= -0.05:
        sentiment = "0"
    elif scores['compound'] >= 0.05:
        sentiment = "1"
    elif -0.05 < scores['compound'] < 0.05:
        sentiment = "2"

    # checking the sentiment and appending it to dictionary
    if sentiment == "0":
        row["negative_count"] = 1
        row["sentiment"] = "negative"
    elif sentiment == "1":
        row["positive_count"] = 1
        row["sentiment"] = "positive"
    elif sentiment == "2":
        row["neutral_count"] = 1
        row["sentiment"] = "neutral"
    return row


def create_json_list(sentences):
    """
    Function to convert sentences to json
    INPUT: List of sentences
    OUTPUT: list of items in json
    """

    lst_json = []
    for sent in sentences:
        row = {}
        row["created_at"] = datetime.datetime.today().strftime('%Y-%m-%d')
        row["sentence"] = sent
        row["positive_count"] = 0
        row["negative_count"] = 0
        row["neutral_count"] = 0

        row = sentiment_score(sent, row)
        lst_json.append(row)
    return lst_json


# function to remove stop words
def remove_stopwords(sentences):
    """
    Function to remove stop words from text
    INPUT: list of sentences
    OUTPUT: List of sentences without stop words
    """
    sent_list_wo_stopwords = []
    for sentence in sentences:
        review = re.sub('\[[^]]*\]', ' ', sentence)
        review = re.sub('[^a-zA-z]', ' ', sentence)
        review = review.lower().split()
        review = [i for i in review if not i in set(stopwords.words('english'))]
        review = ' '.join(review)
        sent_list_wo_stopwords.append(review)

    return sent_list_wo_stopwords


def tfidf_word_highlight(sent_list_wo_stopwords):
    """
    Function to fetch top 15 important keywords using tfidf
    INPUT: array of sentences without stop words
    OUTPUT: list of top 15 elements
    """
    vectorizer = TfidfVectorizer(use_idf=True)
    tfidf_result = vectorizer.fit_transform(sent_list_wo_stopwords)

    scores = zip(vectorizer.get_feature_names(),
                 np.asarray(tfidf_result.sum(axis=0)).ravel())

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores[:15]


# Get tweets of last 15  minutes
def get_tweets(stock_name, minutes, keyword_list):
    """
    Funtion to fetch tweets from twitter
    INPUT: List of important keywords found through tf-idf and time for which tweets are required eg. last 15 min, 30 min
    OUTPUT: List of tweets
    """
    api = authenticate_tweepy()
    endDate = datetime.datetime.now()
    startDate = datetime.timedelta(minutes=minutes)
    startDate = endDate - startDate
    tweets = []
    # search using twitter
    for word in keyword_list:
        tmpTweets = api.search(q=stock_name + " " + word[0], tweet_mode='extended', lang='en')
        for tweet in tmpTweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                tweets.append(tweet)
    tweet_sentences = []
    for i in tweets:
        try:
            tweet_sentences.append(i._json["full_text"])
        except:
            tweet_sentences.append(i._json["text"])
    return tweet_sentences

def send_data(file_name, index_name, lst_json):
    '''
    Function to send data to elasticsearch
    INPUT: file pointer, index name in elasticsearch, json data to send
    OUTPUT: None
    '''
    data = None
    try:
        f = open(file_name)
        data = json.load(f)
        if len(data)>=7:
            del data[0]
    except:
        data = []
    
    dic = {datetime.datetime.today().strftime('%Y-%m-%d') :lst_json }
    data.append(dic)
    with open(file_name, 'w') as fout:
        json.dump(data, fout)
    
    ### send news.json to elasticsearch            
    f=open(file_name)
    elk.create_index(f,index_name)   
    

if __name__ == "__main__":
    # Ticker name for which the data is used
    # In the future you might want to loop over different tickers
    # This is for one ticker
    ticker_name = "NKE"
    stock_name = "Nike"
    filter_time = 86400  # 24 hrs time in seconds
    # news in json
    news_list = filter_yahoo_news(filter_time, ticker_name)
    sentences_news = remove_stopwords(news_list)
    news_json = create_json_list(sentences_news)
    
    ### send data to elasticsearch
    send_data("news.json", "news", news_json)
    
    # tweets in json
    keyword_list = tfidf_word_highlight(sentences_news)
    tweet_sentences = get_tweets(stock_name, 15, keyword_list)
    tweets_json = create_json_list(tweet_sentences)
    
    ### send tweets to elasticsearch
    send_data("tweets.json", "tweets", tweets_json)
 
