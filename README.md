# StockInsight
StockInsight predicts the stock prices using Neural Networks. It uses Elasticsearch, Twitter data, News Headlines and sentiment analysis to find the effect of emotions on the stock price. How much do emotions on twitter and news headlines affect stock price? What could be the price of stock within next 30 minutes? Let's find out...

# About
StockInsight uses Long Short Term Memory to predict the stock price of a stock. StockInsight uses Elasticsearch to store Twitter data. StockInsight analyzes the emotions of what the author writes and does sentiment analysis on the text to determine how the author "feels" about a stock. StockInsight uses tf-idf to find filter out important keywords from the news headlines, it then makes a search on Twitter based on important keywords found in news articles. StockInsight uses Kibana for data visualization and exploration. It also uses Kafka for the simulation of the ra=eal time stock data.

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
* Twitter Developer account(Account creation is Free) you can find steps here.
* Yahoo finance API account(Account creation is Free) You can find link here.
* requests python module
