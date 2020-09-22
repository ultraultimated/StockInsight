

## Data Extraction

Stock Insight gives us prediction for stocks every minute. Thus, the dataset requires per minute stock data for the stocks.
The stock data is fetched using alphavantange API. The data is collected for 15 stocks for the last one month.
Data_extraction.py fetches the stock data for the trading day. The script allows you to get per minute stock data everyday.
The script is executed everyday at midnight since live streaming of stock data requires paid membership.

Alphavantage API allows only 5 request (stocks) per minute and thus it requires few minutes to fetch data for all the stocks.
To know more about the API, visit https://www.alphavantage.co/documentation/

Get alpha vantage API by creating an account on https://www.alphavantage.co/

Since live stock price is not acheivable, to simulate the real time data we consider the previous day data as today's data. Since yesterday's training data is considered as live data, the historical data folder will contain all the datapoints before the previous day whereas simulation data folder consist of previous day's data.

Update the script by changing the date for which you want to fetch data and the list of stocks for which you want to fetch the data.

### Run the script-
On the command line: <b> python data_extraction.py </b>


## Dataset
The alphavantage API fetches stock data which consists of following columns: 
* Date 
* Open price 
* High price
* Low price
* Close price
* Volume

The stock data consists of data from 14th August - 17th Septemeber. The dataset consists of per minute stock data for each stocks. 
We have csv file for each stocks which is updated everyday by running the data_extraction.py file.

## Data Preprocessing
Following steps are performed during the preprocessing stage:
1) Stock prices are predicted only based on the closing price.
2) Standardize the dataset using MinMaxScaler.
3) Split the dataset into train-validation pairs.
4) Create a mapping of last 300 points with the current data point. The current datapoint is predicted based on the last 300 datapoints. 

## LSTM Model

LSTM stands for Long Short-Term Memory which is an artificial recurrent neural network architecture. LSTM's are very good in sequence prediction problems since they are able to store past information.
Thus, they seem to be very good fit for stock predictions since previous price of stock is crucial in predicting it's future price.

LSTM Specifications:
* No of layers - 3 LSTM layers + Dense layer
* Units - 50 units in LSTM layers
* Loss function -  Mean Squared error
* Optimizer -  Adam
* Total parameters - 50,851
* Batch size - 64 

We keep a model checkpoint to save the weights and monitor the validation loss. If the validation loss doesn't decrease it would stop training.

## Predictions

The data was is divided into training and validation set. The training dataset consists of 80% of total data whereas validation data is 20%.

The validation results for the models are as follows:
| Stock | MAE |
| --- | --- |
| NKE (Nike) | 0.276  |
| EXPE (Expedia) | 0.347 |




