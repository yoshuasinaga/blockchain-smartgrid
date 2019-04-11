from flask_login import UserMixin
from web3 import Web3
from app.ethereum import get_smart_contract
from app.utils import timestamp_to_minutes_from_midnight, day_of_timestamp
from app import login
from config import Config

import pandas as pd
from datetime import datetime

class User(UserMixin):
	def __init__(self, w3, addr):
		smart_contract = get_smart_contract(w3, 'CONSUMERS_STORAGE')
		self.id, self.username, self.login_as = smart_contract.functions.getUser().call({'from': Web3.toChecksumAddress(addr)})

	def __repr__(self):
		return '<User {}>'.format(self.username)
		
class BasicModel():
	def __init__(self, w3, contract_addr):
		self.data = None
		self.smart_contract = get_smart_contract(w3, contract_addr)

class DataEntry(BasicModel):
	def __init__(self, w3, addr, today_timestamp):
		BasicModel.__init__(self, w3, 'CONSUMERS_STORAGE')
		self.data = []
		index = self.smart_contract.functions.getStorageLength().call({'from': Web3.toChecksumAddress(addr)}) - 1
		while (index >= 800):
			entry = self.smart_contract.functions.getDataEntry(index).call({'from': Web3.toChecksumAddress(addr)})
			if not today_timestamp <= entry[1]:
				break
			self.data.append(entry)
			index -= 1
		for i in range(48 - len(self.data)):
			self.data.insert(0, ['0', today_timestamp + 1800 * len(self.data), -1, -1, -1])
		columns = ['addr', 'timestamp', 'voltage', 'power', 'energy']
		self.data = pd.DataFrame(self.data, columns=columns)
		self.data['energy'] = self.data['energy'] / 100

	def __repr__(self):
		return 

class DemandPrediction(BasicModel):
	def __init__(self, w3, addr):
		BasicModel.__init__(self, w3, 'CONSUMERS_STORAGE')
		# Process data for prediction
		self.data = pd.DataFrame(columns=['Minutes From Midnight', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Consumption'])
		index = self.smart_contract.functions.getStorageLength().call({'from': Web3.toChecksumAddress(addr)}) - 1
		# Get user's historical data
		while (index >= 0):
			entry = self.smart_contract.functions.getDataEntry(index).call({'from': Web3.toChecksumAddress(addr)})
			# Continue here
			temp_df = pd.DataFrame([[timestamp_to_minutes_from_midnight(entry[1]), entry[4] / 100]], columns=['Minutes From Midnight', 'Consumption'])
			for i in range(7):
				if i == day_of_timestamp(entry[1]):
					temp_df.insert(i + 1, Config.DAY_ENUM[i], [1])
				else:
					temp_df.insert(i + 1, Config.DAY_ENUM[i], [0])
			self.data = pd.concat([self.data, temp_df])
			index -= 1
		users_weight = [Config.INT_WEIGHT for x in range(self.data.shape[0])]
		self.data.insert(9, 'Weight', users_weight)
		self.data = self.data.reset_index(drop=True)

	def __repr__(self):
		return

class PredictionData(BasicModel):
	def __init__(self, w3, addr):
		BasicModel.__init__(self, w3, 'PREDICTION_STORAGE')
		data_list = []
		for time_offset in range(48):
			if addr == Config.ADMIN_UID:
				prediction = self.smart_contract.functions.getMarketPrediction(time_offset).call({'from': Web3.toChecksumAddress(addr)})
			else:
				prediction = self.smart_contract.functions.getUserPrediction(time_offset).call({'from': Web3.toChecksumAddress(addr)})
			data_list.append(prediction[1:])
		self.data = pd.DataFrame(data_list, columns=['timestamp', 'energy'])
		today = datetime.now().date()
		today_timestamp = datetime(today.year, today.month, today.day).timestamp()
		self.data['timestamp'] = self.data['timestamp'].apply(lambda x: today_timestamp + 1800 * x)
		self.data['energy'] = self.data['energy'] / 100

	def __repr__(self):
		return

class PredictionIndex(BasicModel):
	def __init__(self, w3, addr_list):
		BasicModel.__init__(self, w3, 'PREDICTION_STORAGE')
		index_list = []
		for addr in addr_list:
			if len(addr_list) == 1:
				index_list.append(self.smart_contract.functions.getMarketPredictionIndex().call({'from': Web3.toChecksumAddress(addr)}))
			else:
				index_list.append(self.smart_contract.functions.getUserPredictionIndex().call({'from': Web3.toChecksumAddress(addr)}))
		self.data = pd.DataFrame(index_list, columns=['user_id', 'last_predicted'])

	def __repr__(self):
		return

class ConsumptionLimit(BasicModel):
	def __init__(self, w3, addr):
		BasicModel.__init__(self, w3, 'CONSUMERS_STORAGE')
		self.data = {}
		# Need to add logic to handle first-time user
		for time_offset in range(48):
			limit = self.smart_contract.functions.getConsumptionLimit(time_offset).call({'from': Web3.toChecksumAddress(addr)})
			self.data[time_offset] = limit[2] / 100

	def __repr__(self):
		return

class ConsumptionTariff(BasicModel):
	def __init__(self, w3, addr):
		BasicModel.__init__(self, w3, 'PROVIDERS_STORAGE')
		self.data = {}
		for time_offset in range(48):
			tariff = self.smart_contract.functions.getConsumptionCost(time_offset).call({'from': Web3.toChecksumAddress(addr)})
			self.data[time_offset] = tariff[2] / 100

	def __repr__(self):
		return

class Incentive(BasicModel):
	def __init__(self, w3, addr):
		BasicModel.__init__(self, w3, 'GOVERNMENT_STORAGE')
		self.data = {}
		for time_offset in range(48):
			incentive = self.smart_contract.functions.getIncentive(time_offset).call({'from': Web3.toChecksumAddress(addr)})
			self.data[time_offset] = incentive[2] / 100

	def __repr__(self):
		return

@login.user_loader
def load_user(addr):
	# Works with any w3 object
	w3 = Web3(Web3.HTTPProvider(Config.WEB3_CONSUMERS_URI))
	return User(w3, str(addr))