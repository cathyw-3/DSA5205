import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import scipy.stats as stats

def get_yfinance_data(tickers_str, start_date, end_date):
	'''
	tickers_str: tickers with format as a string in "ticker1 ticker2 ticker3 ..."
	start_date: "%Y-%M-%D"
	end_date: "%Y-%M-%D"
	'''
	yf.pdr_override() # <== that's all it takes :-)

	# download dataframe
	data = pdr.get_data_yahoo(tickers_str, start=start_date, end=end_date)
	return data

def store_raw_stock_data(yfinance_data, file_path, ticker_list):
	column_list = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
	data_transfer = pd.DataFrame(columns=['Date', 'Index']+column_list)
	for ticker in ticker_list:
		tmp_data = pd.DataFrame(data=yfinance_data.index, columns=['Date'])
		for column in column_list:
			tmp = pd.DataFrame(yfinance_data[(column, ticker)])
			tmp.columns = tmp.columns.values
			tmp = tmp.reset_index()
			tmp[column] = tmp[(column, ticker)]
			tmp = tmp[['Date', column]]
			tmp_data = tmp_data.merge(tmp, on='Date', how='outer')
		tmp_data['Index'] = ticker
		data_transfer = pd.concat([data_transfer, tmp_data], ignore_index=True)
	data_transfer.to_csv(file_path, index=False)

def calculate_kurtosis_sorted(ticker_list, returns_ratio):
	kurtosis = {}

	for i in range(len(ticker_list)):
		kurtosis[ticker_list[i]] = stats.kurtosis(returns_ratio[ticker_list[i]], fisher=False)
	
	sorted_kurtosis = dict(sorted(kurtosis.items(), key=lambda item : item[1]))
	return sorted_kurtosis

def kurtosis_filter(sorted_kurtosis):
	kur_df = pd.DataFrame.from_dict(sorted_kurtosis, orient='index', columns=['kurtosis'])
	margin = 1.5*(kur_df.describe().loc['75%'][0] - kur_df.describe().loc['25%'][0]) + kur_df.describe().loc['75%'][0]
	filter_res = dict()
	for (key, value) in sorted_kurtosis.items():
		if value <= margin:
			filter_res[key] = value
	
	return filter_res

# get trading indicators -> include 1529 available stocks(be traded for at least one year by January 1, 2022)
indicator_path = "/content/drive/MyDrive/DSA5205/Data/trading_indicators.csv"
trading_indicators = pd.read_csv(indicator_path)
trading_indicators = trading_indicators[['index', 'annual_sharperatio', 'max_drawdown', 'carmarratio']]
ticker_list = list(trading_indicators['index'])
# # get all 1529 information first
# tickers_str = ' '.join(ticker_list)
# data = get_yfinance_data(tickers_str, "2020-01-01", "2022-08-01")
# # you can store the 2020-01-01->2022-08-01 first, change the multi-index into single-index
# file_path = '/content/drive/MyDrive/DSA5205/Raw_Stock_Data.csv'
# store_raw_stock_data(data, file_path, ticker_list)
# # get adj close of current stocks, calculate its return ratio
# # we can store adj close first
# data['Adj Close'].reset_index().to_csv('/content/drive/MyDrive/DSA5205/Data/Stock_Adj_Close.csv', index=False)
Adj_Close_df = pd.read_csv('/content/drive/MyDrive/DSA5205/Data/Stock_Adj_Close.csv').set_index('Date')
returns_ratio = Adj_Close_df.pct_change().fillna(method='bfill')
# filter out stocks with high kurtosis, get 1333 available stocks
sorted_kurtosis = calculate_kurtosis_sorted(ticker_list, returns_ratio)
filter_ticker_list = list(kurtosis_filter(sorted_kurtosis).keys())
# filter out half of stocks using annual sharpe ratio, 666 stock pool
filter_metrics = trading_indicators[trading_indicators.index.isin(filter_ticker_list)].reset_index()
N = len(filter_ticker_list) // 2
Top_N_Sharpe = filter_metrics[['index', 'annual_sharperatio']].sort_values(['annual_sharperatio'], ascending=False).head(N)
new_ticker_list = list(Top_N_Sharpe['index'])
with open('/content/drive/MyDrive/DSA5205/Data/Ticket_Candidates.txt', 'w') as f:
	for name in new_ticker_list:
		f.write(name + "\n")
	f.close()



# get all 666 tickers information
ticker_list = []
with open('/content/drive/MyDrive/DSA5205/Data/Ticket_Candidates.txt', 'r') as f:
	for ticker in f.readlines():
		ticker_list.append(ticker[:-1])

tickers_str = ' '.join(ticker_list)
raw_data = get_yfinance_data(tickers_str, "2020-01-01", "2022-08-01")
file_path = '/content/drive/MyDrive/DSA5205/Data/Raw_Stock_Data.csv'
store_raw_stock_data(raw_data, file_path, ticker_list)

