

# Libraries
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from time import sleep

def fetch_stock_data(stocks):
    """
    Fetches stock data (per min) for last 14 days.
    INPUT: List of stocks
    OUTPUT: CSV files generated in data folder for all the stocks
    """
    cnt=0
    for stock in stocks:
        time=TimeSeries(key="NY2H8A7YOEAYXLMN",output_format='pandas')
        data=time.get_intraday(symbol=stock,interval='1min',outputsize="full")
        stock_df=data[0]
        stock_df.to_csv("Data/"+stock+".csv")
        
        ## API can only fetch data for 5 stocks in a minute 
        cnt+=1
        if cnt==4:
            cnt=0
            sleep(60)
			
def stock_data_daily(stocks,date):
	"""
    Updates the csv files with the current date's data
    INPUT: List of stocks and today's date
    OUTPUT: CSV files generated in data folder for all the stocks
    """
	cnt=0
	for stock in stocks:
		df=pd.read_csv("Data/"+stock+".csv",index_col=0)
		df=df.sort_index()
		time=TimeSeries(key="NY2H8A7YOEAYXLMN",output_format='pandas')
		data=time.get_intraday(symbol=stock,interval='1min',outputsize="full")
		stock_df=data[0].loc[date] 
		stock_df=stock_df.sort_index()
		final_df=pd.concat([df,stock_df])
		final_df.to_csv("Data/"+stock+".csv")
		## API can only fetch data for 5 stocks in a minute 
		cnt+=1
		if cnt==4:
			cnt=0
			sleep(60)
            
stocks=["AAPL","AMRX","AMZN","IBM","NKE","FB","MSFT","GOOGL","WMT","WFC","GS","EXPE","UBER","TWTR","BRK-A"]
stock_data_daily(stocks,'2020-08-28')