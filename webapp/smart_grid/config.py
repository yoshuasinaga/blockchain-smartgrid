import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'blockchain-for-smart-grid'
	SERVER_NAME = os.environ.get('SERVER_NAME')

	ADMIN_UID = os.environ.get('ADMIN_UID')
	ADMIN_PWD = os.environ.get('ADMIN_PWD')

	DAY_ENUM = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

	EXT_WEIGHT = 0.5
	INT_WEIGHT = 2

	# Blockchain nodes' addresses
	WEB3_CONSUMERS_URI = os.environ.get('WEB3_CONSUMERS_URI')
	WEB3_PROVIDERS_URI = os.environ.get('WEB3_PROVIDERS_URI')
	WEB3_GOVERNMENT_URI = os.environ.get('WEB3_GOVERNMENT_URI')

	# Smart Contracts (Consumers)
	CONTRACT_ADDR = {
		'CONSUMERS_STORAGE': '0x64ed73b6fd99d5d682728ba69bdb29650f71d249',
		'PROVIDERS_STORAGE': '0x322f01f3ee7fe4044581cd293a038702d4ee6adf',
		'GOVERNMENT_STORAGE': '0xfd782feaf34b84daaa1f6d54f5db3f0bb1ee2410',
		'PREDICTION_STORAGE': '0x19132a265a6b5a4d4aee21aa562117cd726b7d61'
	}
	ABI = {
		'CONSUMERS_STORAGE': '''[
			{
				"constant": false,
				"inputs": [
					{
						"name": "_username",
						"type": "string"
					},
					{
						"name": "_login_as",
						"type": "string"
					}
				],
				"name": "addUser",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [],
				"name": "getStorageLength",
				"outputs": [
					{
						"name": "",
						"type": "uint256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_time_offset",
						"type": "uint256"
					},
					{
						"name": "_limit",
						"type": "uint256"
					}
				],
				"name": "setConsumptionLimit",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [],
				"name": "kill",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [
					{
						"name": "_index",
						"type": "uint256"
					}
				],
				"name": "getDemandPrediction",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "uint256"
					},
					{
						"name": "",
						"type": "uint256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [],
				"name": "getUser",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "string"
					},
					{
						"name": "",
						"type": "string"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [
					{
						"name": "_index",
						"type": "uint256"
					}
				],
				"name": "getConsumptionLimit",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "uint256"
					},
					{
						"name": "",
						"type": "uint256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [],
				"name": "getPredictionIndex",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "string"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_addr",
						"type": "address"
					},
					{
						"name": "_time_offset",
						"type": "uint256"
					},
					{
						"name": "_prediction",
						"type": "uint256"
					}
				],
				"name": "saveDemandPrediction",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_current_timestamp",
						"type": "uint256"
					},
					{
						"name": "_voltage_consumption",
						"type": "int256"
					},
					{
						"name": "_power_consumption",
						"type": "int256"
					},
					{
						"name": "_energy_consumption",
						"type": "int256"
					}
				],
				"name": "addDataEntry",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [
					{
						"name": "_index",
						"type": "uint256"
					}
				],
				"name": "getDataEntry",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "uint256"
					},
					{
						"name": "",
						"type": "int256"
					},
					{
						"name": "",
						"type": "int256"
					},
					{
						"name": "",
						"type": "int256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_addr",
						"type": "address"
					},
					{
						"name": "_date",
						"type": "string"
					}
				],
				"name": "updatePredictionIndex",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"inputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "constructor"
			}
		]''',
		'PROVIDERS_STORAGE': '''[
			{
				"constant": false,
				"inputs": [],
				"name": "kill",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_time_offset",
						"type": "uint256"
					},
					{
						"name": "_cost",
						"type": "uint256"
					}
				],
				"name": "setConsumptionCost",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [
					{
						"name": "_time_offset",
						"type": "uint256"
					}
				],
				"name": "getConsumptionCost",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "uint256"
					},
					{
						"name": "",
						"type": "uint256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "constructor"
			}
		]''',
		'GOVERNMENT_STORAGE': '''[
			{
				"constant": false,
				"inputs": [],
				"name": "kill",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_time_offset",
						"type": "uint256"
					},
					{
						"name": "_incentive",
						"type": "int256"
					}
				],
				"name": "setIncentive",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [
					{
						"name": "_time_offset",
						"type": "uint256"
					}
				],
				"name": "getIncentive",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "uint256"
					},
					{
						"name": "",
						"type": "int256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "constructor"
			}
		]''',
		'PREDICTION_STORAGE': '''[
			{
				"constant": false,
				"inputs": [
					{
						"name": "_addr",
						"type": "address"
					},
					{
						"name": "_date",
						"type": "string"
					}
				],
				"name": "updateUserPredictionIndex",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [],
				"name": "kill",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [],
				"name": "getUserPredictionIndex",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "string"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_addr",
						"type": "address"
					},
					{
						"name": "_time_offset",
						"type": "uint256"
					},
					{
						"name": "_prediction",
						"type": "uint256"
					}
				],
				"name": "saveUserPrediction",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [],
				"name": "getMarketPredictionIndex",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "string"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [
					{
						"name": "_index",
						"type": "uint256"
					}
				],
				"name": "getUserPrediction",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "uint256"
					},
					{
						"name": "",
						"type": "uint256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_date",
						"type": "string"
					}
				],
				"name": "updateMarketPredictionIndex",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": false,
				"inputs": [
					{
						"name": "_time_offset",
						"type": "uint256"
					},
					{
						"name": "_prediction",
						"type": "uint256"
					}
				],
				"name": "saveMarketPrediction",
				"outputs": [],
				"payable": false,
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"constant": true,
				"inputs": [
					{
						"name": "_index",
						"type": "uint256"
					}
				],
				"name": "getMarketPrediction",
				"outputs": [
					{
						"name": "",
						"type": "address"
					},
					{
						"name": "",
						"type": "uint256"
					},
					{
						"name": "",
						"type": "uint256"
					}
				],
				"payable": false,
				"stateMutability": "view",
				"type": "function"
			}
		]'''
	}

			