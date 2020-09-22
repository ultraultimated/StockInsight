[![Build Status](https://travis-ci.org/ultraultimated/StockInsight.svg?branch=master)](https://travis-ci.org/ultraultimated/StockInsight)
[![GitHub issues](https://img.shields.io/github/issues/ultraultimated/StockInsight)](https://github.com/ultraultimated/StockInsight/issues)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ultraultimated/StockInsight)
![GitHub contributors](https://img.shields.io/github/contributors/ultraultimated/StockInsight)
[![DOI](https://zenodo.org/badge/291098939.svg)](https://zenodo.org/badge/latestdoi/291098939)

# StockInsight
StockInsight predicts the stock prices using Neural Networks. It uses Elasticsearch, Twitter data, News Headlines and sentiment analysis to find the effect of emotions on the stock price. How much do emotions on twitter and news headlines affect stock price? What could be the price of stock within next 30 minutes? Let's find out...

# Click on the image below to see the video
[![Watch the video](https://img.youtube.com/vi/Fc5fHP2nowA/hqdefault.jpg)](https://youtu.be/Fc5fHP2nowA)
# About
StockInsight uses Long Short Term Memory to predict the stock price of a stock. StockInsight uses Elasticsearch to store Twitter data. StockInsight analyzes the emotions of what the author writes and does sentiment analysis on the text to determine how the author "feels" about a stock. StockInsight uses tf-idf to filter out important keywords from the news headlines, it then makes a search on Twitter based on important keywords found in news articles. StockInsight uses Kibana for data visualization and exploration. It also uses Kafka for the simulation of the real time stock data.

![alt text](https://github.com/ultraultimated/StockInsight/blob/master/images/Stock_Insight.jpeg)

# Requirements
* Elasticsearch 7.x
* Kakfa 2.6.x
* Python 3.x
* Kibana 8.x
* Tensorflow 2.x
* Keras 2.x
* Tweepy python module
* Elasticsearch python module
* vaderSentiment analyzer
* Twitter Developer account(Account creation is Free) you can find steps [here](https://www.extly.com/docs/autotweetng_joocial/tutorials/how-to-auto-post-from-joomla-to-twitter/apply-for-a-twitter-developer-account/#apply-for-a-developer-account).
* Yahoo finance API account(Account creation is Free) You can find link [here](
https://rapidapi.com/blog/how-to-use-the-yahoo-finance-api/).
* requests python module

# Installing Kafka
* To install kafka in ubuntu follow the steps [here](https://linuxhint.com/install-apache-kafka-ubuntu/)
* To install Kafka in windows follow the steps [here](https://dzone.com/articles/running-apache-kafka-on-windows-os)

# Installing ELK
* To install ELK in ubuntu follow the steps [here](https://logz.io/learn/complete-guide-elk-stack/#installing-elk)
* To install ELK in windows follow the steps [here](https://logz.io/blog/installing-the-elk-stack-on-windows/)

# How to see predictions
Start Kafka depending on the installation location:
```
> /opt/Kafka/kafka_2.13-2.6.0/bin/zookeeper-server-start.sh /opt/Kafka/kafka_2.13-2.6.0/config/zookeeper.properties 

```

Start predictor in Terminal #2:
```
cd code
python predictor.py
```

Start app in Terminal #3:
```
> cd code
> python app.py
```

Start the pipeline for ELK in Terminal #4:
```
> cd code
> python pipeline.py
```

# How to train the LSTM Model
```
cd code
python train.py
```
