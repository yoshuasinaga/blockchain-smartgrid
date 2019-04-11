from app import app, login
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.models import User, DataEntry, ConsumptionLimit, ConsumptionTariff, Incentive, PredictionData
from app.ethereum import get_smart_contract
from app.utils import login_required_custom, df_to_dict
from app.prediction import predict_demand
from web3 import Web3

from datetime import datetime
import pandas as pd
import json

@app.route('/')
@app.route('/home')
@login_required_custom(login_as='consumer')
def home():
	# Initiate w3 object
	w3 = Web3(Web3.HTTPProvider(app.config['WEB3_CONSUMERS_URI']))
	# Get today's timestamp at 00:00
	today = datetime.now().date()
	today_timestamp = datetime(today.year, today.month, today.day).timestamp()
	# Get data entries
	data_entries = DataEntry(w3, current_user.id, today_timestamp)
	data_entries = df_to_dict(data_entries.data[['timestamp', 'energy']])
	# Get demand prediction
	prediction_df = PredictionData(w3, current_user.id).data
	prediction = df_to_dict(prediction_df)
	return render_template('home_consumers.html', title='Home', subdomain ='', data_entries=data_entries, prediction=prediction)

@app.route('/set_limit', methods=['GET', 'POST'])
@login_required_custom(login_as='consumer')
def set_limit():
	# Initiate w3 object
	w3 = Web3(Web3.HTTPProvider(app.config['WEB3_CONSUMERS_URI']))
	if request.method == 'POST':
		consumption_limit = json.loads(request.form.get('values'))['data']
		password = request.form.get('password')
		# Save user's consumption limit
		smart_contract = get_smart_contract(w3, 'CONSUMERS_STORAGE')
		if w3.personal.unlockAccount(Web3.toChecksumAddress(current_user.id), password):
			for time_offset in range(47):
				smart_contract.functions.setConsumptionLimit(time_offset, int(consumption_limit[time_offset] * 100)).transact({'from': Web3.toChecksumAddress(current_user.id)})
			tx_hash = smart_contract.functions.setConsumptionLimit(47, int(consumption_limit[47] * 100)).transact({'from': Web3.toChecksumAddress(current_user.id)})
			w3.eth.waitForTransactionReceipt(tx_hash, timeout=300)
			flash("Your changes have been saved!")
		else:
			flash("Invalid password. Your changes have not been saved.")
	# Get today's timestamp at 00:00
	today = datetime.now().date()
	today_timestamp = datetime(today.year, today.month, today.day).timestamp()
	# Get user's consumption limit
	consumption_limit = ConsumptionLimit(w3, current_user.id)
	# Get consumption tariff
	consumption_tariff = ConsumptionTariff(w3, current_user.id)
	# Get incentive
	incentive = Incentive(w3, current_user.id)
	# Dummy data for prediction
	prediction_df = PredictionData(w3, current_user.id).data
	prediction = df_to_dict(prediction_df)
	return render_template('set_limit_new.html', title='Set Consumption Limit', subdomain='', data_entries=consumption_limit.data, prediction=prediction, consumption_tariff=consumption_tariff.data, incentive=incentive.data)

@app.route('/login', subdomain='government')
@app.route('/login', subdomain='provider')
def route_login():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	# Implement login functionalities here
	if current_user.is_authenticated:
		if current_user.login_as == 'consumer':
			return redirect(url_for('home'))
		else:
			return redirect(url_for(current_user.login_as + '_home'))
	form = LoginForm()
	if form.validate_on_submit():
		# Determine user type from login_as
		if form.login_as.data == 'consumer':
			w3 = Web3(Web3.HTTPProvider(app.config['WEB3_CONSUMERS_URI']))
			subdomain = ''
		else:
			if form.login_as.data == 'provider':
				w3 = Web3(Web3.HTTPProvider(app.config['WEB3_PROVIDERS_URI']))
			else:
				w3 = Web3(Web3.HTTPProvider(app.config['WEB3_GOVERNMENT_URI']))
			subdomain = form.login_as.data
		if form.username.data in [x.lower() for x in w3.eth.accounts] and w3.personal.unlockAccount(Web3.toChecksumAddress(form.username.data), form.password.data):
			user = User(w3, form.username.data)
			login_user(user, remember=form.remember_me.data)
			flash('Login requested for user {}. Successful!'.format(user.username))
			next_page = request.args.get('next')
			if not next_page or app.config['SERVER_NAME'] not in url_parse(next_page).netloc:
				next_page = url_for((subdomain + '_' if subdomain != '' else '') + 'home')
			return redirect(next_page)
		else:
			flash('Invalid username or password. Login failed!')
			return redirect(url_for('login'))
	return render_template('login.html', title="Sign In", form=form, subdomain='')

@app.route('/logout', subdomain='government')
@app.route('/logout', subdomain='provider')
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/', subdomain='provider')
@app.route('/home', subdomain='provider')
@login_required_custom(login_as='provider')
def provider_home():
	# Initiate w3 object
	w3 = Web3(Web3.HTTPProvider(app.config['WEB3_CONSUMERS_URI']))
	# Dummy data for prediction
	prediction_df = PredictionData(w3, app.config['ADMIN_UID']).data
	prediction = df_to_dict(prediction_df)
	return render_template('home_providers.html', title='Home', subdomain='provider', data_entries='', prediction=prediction)


@app.route('/set_tariff', subdomain='provider', methods=['GET', 'POST'])
def set_tariff():
	# Initiate w3 object
	w3 = Web3(Web3.HTTPProvider(app.config['WEB3_PROVIDERS_URI']))
	if request.method == 'POST':
		consumption_tariff = json.loads(request.form.get('values'))['data']
		password = request.form.get('password')
		# Save user's consumption limit
		smart_contract = get_smart_contract(w3, 'PROVIDERS_STORAGE')
		if w3.personal.unlockAccount(Web3.toChecksumAddress(current_user.id), password):
			for time_offset in range(47):
				smart_contract.functions.setConsumptionCost(time_offset, int(consumption_tariff[time_offset] * 100)).transact({'from': Web3.toChecksumAddress(current_user.id)})
			tx_hash = smart_contract.functions.setConsumptionCost(47, int(consumption_tariff[47] * 100)).transact({'from': Web3.toChecksumAddress(current_user.id)})
			w3.eth.waitForTransactionReceipt(tx_hash, timeout=300)
			flash("Your changes have been saved!")
		else:
			flash("Invalid password. Your changes have not been saved.")
	# Get current tariff
	consumption_tariff = ConsumptionTariff(w3, current_user.id)
	# Get current incentive
	incentive = Incentive(w3, current_user.id)
	# Dummy data for prediction
	prediction_df = PredictionData(w3, app.config['ADMIN_UID']).data
	prediction = df_to_dict(prediction_df)
	return render_template('set_tariff.html', title='Home', subdomain='provider', prediction=prediction, consumption_tariff=consumption_tariff.data, incentive=incentive.data)

@app.route('/', subdomain='government')
@app.route('/home', subdomain='government')
@login_required_custom(login_as='government')
def government_home():
	# Initiate w3 object
	w3 = Web3(Web3.HTTPProvider(app.config['WEB3_CONSUMERS_URI']))
	prediction_df = PredictionData(w3, app.config['ADMIN_UID']).data
	prediction = df_to_dict(prediction_df)
	return render_template('home_government.html', title='Home', subdomain='government', data_entries='', prediction=prediction)

@app.route('/set_incentive', subdomain='government', methods=['GET', 'POST'])
def set_incentive():
	# Initiate w3 object
	w3 = Web3(Web3.HTTPProvider(app.config['WEB3_GOVERNMENT_URI']))
	if request.method == 'POST':
		incentive = json.loads(request.form.get('values'))['data']
		password = request.form.get('password')
		# Save user's consumption limit
		smart_contract = get_smart_contract(w3, 'GOVERNMENT_STORAGE')
		if w3.personal.unlockAccount(Web3.toChecksumAddress(current_user.id), password):
			for time_offset in range(47):
				smart_contract.functions.setIncentive(time_offset, int(incentive[time_offset] * 100)).transact({'from': Web3.toChecksumAddress(current_user.id)})
			tx_hash = smart_contract.functions.setIncentive(47, int(incentive[47] * 100)).transact({'from': Web3.toChecksumAddress(current_user.id)})
			w3.eth.waitForTransactionReceipt(tx_hash, timeout=300)
			flash("Your changes have been saved!")
		else:
			flash("Invalid password. Your changes have not been saved.")
	# Get current tariff
	consumption_tariff = ConsumptionTariff(w3, current_user.id)
	# Get current incentive
	incentive = Incentive(w3, current_user.id)
	prediction_df = PredictionData(w3, app.config['ADMIN_UID']).data
	prediction = df_to_dict(prediction_df)
	return render_template('set_incentive.html', title='Home', subdomain='government', prediction=prediction, consumption_tariff=consumption_tariff.data, incentive=incentive.data)

