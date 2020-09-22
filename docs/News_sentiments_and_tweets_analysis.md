# Twitter developer account
A really good and complete explanation to create twiteer developer account can be found [here](https://www.extly.com/docs/autotweetng_joocial/tutorials/how-to-auto-post-from-joomla-to-twitter/apply-for-a-twitter-developer-account/#apply-for-a-developer-account)

# Yahoo rapid api account
The steps to create a yahoo rapid api account can be found [here](https://rapidapi.com/blog/how-to-use-the-yahoo-finance-api/)

# Prerequisites
```
python -m spacy download en_core_web_lg() --> Downloads spacy models 
nltk.download('vader_lexicon')
```

# Flow of pipeline.py
1) Fetch yahoo news using filter_yahoo_news() function. This function fetches the news headline and summary and returns a list with these data. We use a window of 24 hours to fetch latest news.
2) We remove stop words from this list.
3) We predict compound sentiment of all the data in the list and add them to a news.json file.
4) We then send data to elasticsearch using this json
5) To highlight important keywords in the news, we use tfidf_word_hightlight() function. This function will mark important keywords from the news using tf-idf and returns a list containing top 15 words.
6) This list is then used by the get_tweets() function to filter tweets based on stock name and the highlighted words for the last 30 minutes.
7) We remove stop words from the tweets and perform sentiment analysis to find out the current trends for the stock and create a json file containing these.
8) We then send data to elasticsearch using this json.

# Cron job
Since the code should run in every 30 minutes, we setup a cron job 
1) Open a terminal and type following command<br>
``` crontab -e```
2) Type the following command in the file<br>
```*/30 * * * * /path/to/python /path/to/pipeline.py >> ~/cron.log 2>&1 ```
