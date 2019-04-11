import pandas as pd
import atexit
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from datetime import date
from config import Config
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from web3 import Web3

from app.models import DemandPrediction, PredictionIndex
from app.data import load_ext_data
from app.ethereum import get_smart_contract


def get_to_predict():
	to_predict = pd.DataFrame([i * 30 for i in range(48)], columns=['Minutes From Midnight'])
	today = date.today()
	one_matrix = [1 for x in range(48)]
	zero_matrix = [0 for x in range(48)]
	for i in range(7):
		if i == today.weekday():
			to_predict.insert(i + 1, Config.DAY_ENUM[i], one_matrix)
		else:
			to_predict.insert(i + 1, Config.DAY_ENUM[i], zero_matrix)
	return to_predict

def predict_demand(df):
	# Return empty prediction if there is no data to predict with
	try:
		svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1, epsilon=0.001)
		X = df[['Minutes From Midnight', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']].values
		y = df['Consumption']
		svr_model = svr_rbf.fit(X, y, sample_weight=df['Weight'])
		# Minutes from midnight to predict
		to_predict = get_to_predict()
		svr_y = svr_model.predict(to_predict.values)
		time_offsets = [i for i in range(48)]
		data = list(zip(time_offsets, svr_y))
		result_df = pd.DataFrame(data, columns=['time_offset', 'energy'])
		return result_df
	except ValueError:
		return pd.DataFrame(columns=['time_offset', 'energy'])

def schedule_predictions(w3, user_list):
	# Run once on setup
	run_user_predictions(w3, user_list)
	run_market_predictions(w3)
	# Set up scheduler to run at 00:00 every day
	scheduler = BackgroundScheduler()
	user_prediction_job = scheduler.add_job(func=run_user_predictions, args=[w3, user_list], trigger='interval', start_date=(date.today() + timedelta(days=1)), days=1)
	market_prediction_job = scheduler.add_job(func=run_market_predictions, args=[w3], trigger='interval', start_date=(date.today() + timedelta(days=1)), days=1)
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

def run_user_predictions(w3, user_list):
	print('Running prediction for users')
	# Read prediction index
	pred_index = PredictionIndex(w3, user_list)
	index = pred_index.data
	to_predict = []
	if (not index.empty):
		to_predict.extend(index[index['last_predicted'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date() if x else date(1970, 1, 1)) < date.today()]['user_id'].values)
	# Predict users
	for user in to_predict:
		print(user)
		# Get prediction data
		user_data = DemandPrediction(w3, user)
		prediction_df = predict_demand(user_data.data)
		save_prediction(w3, user, prediction_df, 'user')
	if len(to_predict):
		new_index = pd.DataFrame(to_predict, columns=['user_id'])
		new_index['last_predicted'] = date.today()
		save_prediction_index(w3, new_index, 'user')
	else:
		print('No user to predict!')

def run_market_predictions(w3):
	print('Running prediction for market')
	# Read prediction index file
	pred_index = PredictionIndex(w3, [Config.ADMIN_UID])
	index = pred_index.data
	if index[index['user_id'] == Web3.toChecksumAddress(Config.ADMIN_UID)]['last_predicted'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date() if x else date(1970, 1, 1)).values[0] < date.today():
		market_data = load_ext_data()
		prediction_df = predict_demand(market_data)
		save_prediction(w3, None, prediction_df, 'market')
		new_index = pd.DataFrame([['market', date.today()]], columns=['user_id', 'last_predicted'])
		save_prediction_index(w3, new_index, 'market')
	else:
		print('No pending market prediction!')

def save_prediction(w3, addr, df, pred_type):
	smart_contract = get_smart_contract(w3, 'PREDICTION_STORAGE')
	w3.personal.unlockAccount(Web3.toChecksumAddress(Config.ADMIN_UID), Config.ADMIN_PWD)
	for index, row in df.iterrows():
		if (pred_type == 'user'):
			smart_contract.functions.saveUserPrediction(Web3.toChecksumAddress(addr), int(row['time_offset']), int(row['energy'] * 100)).transact({'from': Web3.toChecksumAddress(Config.ADMIN_UID)})
		else:
			smart_contract.functions.saveMarketPrediction(int(row['time_offset']), int(row['energy'] * 100)).transact({'from': Web3.toChecksumAddress(Config.ADMIN_UID)})

def save_prediction_index(w3, df, pred_type):
	smart_contract = get_smart_contract(w3, 'PREDICTION_STORAGE')
	w3.personal.unlockAccount(Web3.toChecksumAddress(Config.ADMIN_UID), Config.ADMIN_PWD)
	for index, row in df.iterrows():
		if (pred_type == 'user'):
			smart_contract.functions.updateUserPredictionIndex(Web3.toChecksumAddress(row['user_id']), str(row['last_predicted'])).transact({'from': Web3.toChecksumAddress(Config.ADMIN_UID)})
		else:
			smart_contract.functions.updateMarketPredictionIndex(str(row['last_predicted'])).transact({'from': Web3.toChecksumAddress(Config.ADMIN_UID)})

	