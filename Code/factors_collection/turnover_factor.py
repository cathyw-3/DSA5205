import pandas as pd

def Turnover_range(df, day):
	month = day // 30
	tmp_df = raw_stock_data.groupby(['Index']).rolling(day, on='Date')['Turnover'].sum().reset_index()
	tmp_df[f'Turnover_{month}m'] = tmp_df['Turnover']
	tmp_df = tmp_df[['Index', 'Date', f'Turnover_{month}m']]

	return df.merge(tmp_df, on=['Index', 'Date'])

# get all tickets
ticker_list = []
with open('/content/drive/MyDrive/DSA5205/Data/Ticket_Candidates.txt', 'r') as f:
	for ticker in f.readlines():
		ticker_list.append(ticker[:-1])

# calculate turnover ratio = Volume / floatShares
new_floatShares_df = pd.read_csv('/content/drive/MyDrive/DSA5205/Data/New_floatShares.csv')
raw_stock_data = pd.read_csv('/content/drive/MyDrive/DSA5205/Data/Raw_Stock_Data.csv')
raw_stock_data['YearMonth'] = raw_stock_data.Date.map(lambda x: '-'.join(x.split('-')[:-1]))
raw_stock_data = raw_stock_data[['Date', 'Index', 'Volume', 'YearMonth']]
raw_stock_data = raw_stock_data.merge(new_floatShares_df, on=['YearMonth','Index'], how='outer')
raw_stock_data['Turnover'] = raw_stock_data['Volume'] / raw_stock_data['floatShares']
raw_stock_data = raw_stock_data[['Date', 'Index', 'Volume', 'floatShares', 'Turnover']]

# sum of turnover ratio with recent 1-month, 2-month, 3-month
# 1-month
turnover_df = Turnover_range(raw_stock_data, 30)
# 2-month
turnover_df = Turnover_range(turnover_df, 60)
# 3-month
turnover_df = Turnover_range(turnover_df, 90)
final_df = turnover_df[turnover_df.Date.between('2021-01-01', '2022-08-01')]
final_df.to_csv('/content/drive/MyDrive/DSA5205/Turnover_Factor.csv', index=False)