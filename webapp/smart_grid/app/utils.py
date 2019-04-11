from functools import wraps
from flask_login import current_user
from flask import url_for, redirect, flash
from datetime import datetime

# Define a custom login_required decorator function
# Asserts users' role when accessing certain pages
def login_required_custom(login_as=None):
	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			if not current_user.is_authenticated:
				flash('Please login to view this page.')
				return redirect(url_for('login'))
			if ((current_user.login_as != login_as) and login_as != None):
				flash('You do not have permission to view this page.')
				return redirect(url_for('login'))
			return fn(*args, **kwargs)
		return decorated_view
	return wrapper

def df_to_dict(df):
	return dict(df.to_dict('split')['data'])

def day_of_timestamp(timestamp):
	return datetime.fromtimestamp(timestamp).weekday()

def timestamp_to_minutes_from_midnight(timestamp):
	time = datetime.fromtimestamp(timestamp)
	return 60 * time.hour + time.minute

def hour_minute_to_minutes_from_midnight(hour_minute):
	time = datetime.strptime(hour_minute, '%H:%M')
	return 60 * time.hour + time.minute