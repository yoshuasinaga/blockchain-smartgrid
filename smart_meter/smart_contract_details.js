module.exports = {
	//address: "0x64ed73b6fd99d5d682728ba69bdb29650f71d249",
	address: "0x72692aaaf9e8e2a9889430010cb6b9b3255cf12a",
	abi: Array([
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
				])[0]
};