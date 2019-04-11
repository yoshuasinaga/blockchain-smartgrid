import pandas as pd

from datetime import datetime, date, timedelta
from app.utils import hour_minute_to_minutes_from_midnight
from config import Config

DAY_ENUM = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def get_data(file_addr):
	# Process dataset from EMA
	file = pd.read_excel(file_addr, usecols=[0, 1, 4, 7, 10, 13, 16, 19], header=2).drop([0,1]).reset_index(drop=True).drop(range(48, 54))

	df = pd.DataFrame(columns=['Minutes From Midnight', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Consumption'])

	one_matrix = [1 for x in range(48)]
	zero_matrix = [0 for x in range(48)]

	for day in range(0, 7):
		temp_df = pd.DataFrame(file[['Period Ending Time', DAY_ENUM[day]]])
		temp_df.columns = ['Minutes From Midnight', 'Consumption']
		for i in range(0, 7):
			if i == day:
				temp_df.insert(i + 1, DAY_ENUM[i], one_matrix)
			else:
				temp_df.insert(i + 1, DAY_ENUM[i], zero_matrix)
		df = pd.concat([df, temp_df])

	return df

def all_files(year):
	d = date(year, 1, 1)
	d += timedelta(days=(7 - d.weekday()) % 7)
	while (d.year == year) and (d < date(2019, 2, 4)):
		yield 'app/static/data/' + d.strftime('%Y%m%d') + '.xls'
		d += timedelta(days=7)

def load_ext_data():
	# Get all files
	file_addrs = []
	for file in all_files(2018):
		file_addrs.append(file)
	for file in all_files(2019):
		file_addrs.append(file)

	# Get data from all files
	all_data = pd.DataFrame(columns=['Minutes From Midnight', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Consumption'])
	for file_addr in file_addrs:
		all_data = pd.concat([all_data, get_data(file_addr)])
	all_data = all_data.reset_index(drop=True)

	# Convert timestamp into minutes from midnight
	all_data['Minutes From Midnight'] = all_data['Minutes From Midnight'].apply(lambda x: hour_minute_to_minutes_from_midnight(x))
	ext_weight = [Config.EXT_WEIGHT for x in range(all_data.shape[0])]
	all_data.insert(9, 'Weight', ext_weight)
	return all_data

