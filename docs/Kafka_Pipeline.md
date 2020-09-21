# Real-time Simulation with Apache Kafka

Most of the stock market APIs have a paid plan to fetch the data in real-time. So to keep the project free and easy to use for everyone without limiting the real-time feature we have used Apache Kafka.

So the idea is that we will have the data for the previous day stored locally and then using Apache Kafka, we will send this data minute-by-minute to the trained LSTM model. That is, we will simulate the data as if it is coming in real-time to the prediction model. In the future, if we decide to switch to use some API to provide this data in real-time, we just have to change the endpoint information in the app.py file.

## How is it done?
Start our app using :
```
python app.py
```
### Note: Make sure to start the Kafka Server first. (See the README for more details)

When our app starts, it initiates a producer and a consumer to send and receive a message respectively. They continuously listen to the topic 'app_messages'. 

In the app.py, the producer sends the data to the 'app_messages' topic and the consumer listens on this topic until the 'prediction' attribute is set for that message.

Similarly, in predictor.py, the consumer listens on app_messages to read the 'data' attribute. This data attribute after proper transformation is sent to the model for prediction. Once we get the prediction, the producer writes this prediction to app_messages with the 'prediction' attribute.

And finally, this prediction is read inside app.py by the consumer.