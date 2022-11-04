import pandas as pd
from tqdm import tqdm

ticker_list = []
with open('/content/drive/MyDrive/DSA5205/Data/Ticket_Candidates.txt', 'r') as f:
	for ticker in f.readlines():
		ticker_list.append(ticker[:-1])

# # get current floatShares
# floatShares = {}
# for ticker in ticker_list:
	# stock_info = yf.Ticker(ticker).info
	# if 'floatShares' in stock_info:
		# floatShares[ticker] = stock_info['floatShares']
# floatShares_df = pd.DataFrame.from_dict(data=floatShares, orient='index', columns=['floatShares']).reset_index()
# floatShares_df['Index'] = floatShares_df['index']
# floatShares_df = floatShares_df[['Index', 'floatShares']]
# floatShares_df.to_csv('/content/drive/MyDrive/DSA5205/Data/floatShares.csv')

# read current floatShares
current_floatShares = pd.read_csv('/content/drive/MyDrive/DSA5205/Data/floatShares.csv')[['Index','floatShares']]
# read past floatShares
sharing_dict = pd.read_pickle('/content/drive/MyDrive/DSA5205/Data/sharing_values.pkl')

New_floatShares_df = pd.DataFrame(columns=['YearMonth','Index','floatShares'])
month_range = ['01','02','03','04','05','06','07','08','09','10','11','12']
for ticker in tqdm(ticker_list):
	tmp_dict = {}
	for year in (2020, 2021):
		for month in month_range:
		tmp_dict[str(year)+'-'+month] = None
	for month in month_range[:7]:
		tmp_dict["2022-"+month] =None
  
	if ticker in sharing_dict:
		tmp_df = sharing_dict[ticker]
		tmp_df['year'] = tmp_df.date.map(lambda x : str(x).split('-')[0])
		tmp_df['year_int'] = tmp_df.date.map(lambda x : int(str(x).split('-')[0]))
		tmp_df['month'] = tmp_df.date.map(lambda x : str(x).split('-')[1])
		tmp_df['month_int'] = tmp_df.date.map(lambda x : int(str(x).split('-')[1]))

		for key, value in tmp_dict.items():
			year, month = key.split('-')
			season = int(month) // 3 if int(month) % 3 else int(month) / 3 - 1
			nxt_season = (season + 1) % 4
			nxt_year = int(year) if nxt_season else int(year) + 1
			min_month = nxt_season * 3 + 1
			max_month = nxt_season * 3 + 3
			# print(tmp_df[(tmp_df.year_int==nxt_year) & (min_month<=tmp_df.month_int) & (tmp_df.month_int>=max_month)])
			if len(tmp_df[(tmp_df.year_int==nxt_year) & (min_month<=tmp_df.month_int) & (tmp_df.month_int<=max_month)]) != 0:
				# print(tmp_df[(tmp_df.year_int==nxt_year) & (min_month<=tmp_df.month_int) & (tmp_df.month_int<=max_month)]['outstanding_share'].iloc[0])
				tmp_dict['-'.join([year,month])] = \
					tmp_df[(tmp_df.year_int==nxt_year) & (min_month<=tmp_df.month_int) & (tmp_df.month_int<=max_month)]['outstanding_share'].iloc[0]
			res_df = pd.DataFrame.from_dict(tmp_dict, orient='index', columns=['floatShares']).reset_index()
			res_df['Index'] = ticker
			res_df['YearMonth'] = res_df['index']
			res_df = res_df[['YearMonth','Index','floatShares']]
			res_df = res_df.fillna(method='bfill')
			if ticker in current_floatShares.Index.unique() and np.isnan(current_floatShares[current_floatShares.Index==ticker]['floatShares'].iloc[0]) == False:
				res_df = res_df.fillna(current_floatShares[current_floatShares.Index==ticker]['floatShares'].iloc[0])
			else:
				res_df = res_df.fillna(method='ffill')
	else:
		res_df = pd.DataFrame.from_dict(tmp_dict, orient='index', columns=['floatShares']).reset_index()
		res_df['Index'] = ticker
		res_df['YearMonth'] = res_df['index']
		res_df = res_df[['YearMonth','Index','floatShares']]
		if ticker in current_floatShares.Index.unique() and np.isnan(current_floatShares[current_floatShares.Index==ticker]['floatShares'].iloc[0]) == False:
			res_df = res_df.fillna(current_floatShares[current_floatShares.Index==ticker]['floatShares'].iloc[0])
	New_floatShares_df = pd.concat([New_floatShares_df, res_df])

New_floatShares_df.to_csv('/content/drive/MyDrive/DSA5205/Data/New_floatShares.csv', index=False)
