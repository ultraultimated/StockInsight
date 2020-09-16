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
        time=TimeSeries(key="Enter alphavantage key",output_format='pandas')
        data=time.get_intraday(symbol=stock,interval='1min',outputsize="full")
        stock_df=data[0]
        stock_df.to_csv("Data/Historical_Data/"+stock+".csv")
        
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
	
	Simulation Data consists of last trading day and Historical Data consists of stock data before that day.
	
    """
	cnt=0
	for stock in stocks:
		df=pd.read_csv("Data/Historical_Data/"+stock+".csv",index_col=0)
		df=df.sort_index()
		time=TimeSeries(key="Enter alphavantage key",output_format='pandas')
		data=time.get_intraday(symbol=stock,interval='1min',outputsize="full")
		stock_df=data[0].loc[date]
		stock_df=stock_df.sort_index()
		final_df=pd.concat([df,stock_df])
		
		##Comment the below line when updating simulation data
		final_df.to_csv("Data/Historical_Data/"+stock+".csv")
		stock_df.to_csv("Data/Simulation_Data/"+stock+".csv")
		
		## API can only fetch data for 5 stocks in a minute 
		cnt+=1
		if cnt==4:
			cnt=0
			sleep(60)
  
def main():
	"""
	Update the stocks list for the stocks for which you want historical data.
	Run fetch_stock_data to fetch last 15 days data from the present day.
	Run stock_data_daily to get data for the query date.
	
	"""

	stocks=["NKE","EXPE"]
	#fetch_stock_data(stocks)
	#stocks=["NKE"]
	present_day='2020-09-15'

	stock_data_daily(stocks,present_day)
	
main()