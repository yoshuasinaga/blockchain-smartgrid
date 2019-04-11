// Import modbus-serial package to handle MODBUS-RTU protocol
let modbusRTU = require('modbus-serial');
// Import web3 package, Ethereum Web3 API for JavaScript
let Web3 = require('web3');
// Import smart contract details and user credentials
let smart_contract = require('./smart_contract_details.js');
let user_cred = require('./user_cred.js');

// Initialize Modbus RTU Client
const client = new modbusRTU;

// RS485 Port
const RTU_PORT = "/dev/ttyUSB0";
// Active Voltage Address
const VOLTAGE_ADDR = 305;
// Active Power Address
const POWER_ADDR = 321;
// Active Energy Address
const ENERGY_ADDR = 40961;

// Define variables for readings
let current_timestamp, voltage_value, power_value, energy_value;

// Connect to Modbus RTU
console.log('Connecting to ModbusRTU...');
client.connectRTUBuffered(RTU_PORT, {baudRate: 9600, parity: 'even'});
console.log('ModbusRTU connection established!')

// Store voltage, power and energy readings in a 30-minute interval
setInterval(async function() {
	// Establish connection to Ethereum network and smart contract
	var web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));
	var consumers_storage = new web3.eth.Contract(smart_contract.abi, smart_contract.address)
	// Read values from smart meter
	var current_timestamp = (new Date().setHours(0, 0, 0, 0) + Math.floor((new Date().getTime() - new Date().setHours(0, 0, 0, 0)) / 1800000) * 1800000) / 1000;
	await client.readHoldingRegisters(VOLTAGE_ADDR, 1).then(function(value) {
		voltage_value = value.data[0];
	});
	await client.readHoldingRegisters(POWER_ADDR, 1).then(function(value) {
		power_value = value.data[0];
	});
	await client.readHoldingRegisters(ENERGY_ADDR, 1).then(function(value) {
		energy_value = value.data[0];
	});
	// Unlock Ethereum account
	web3.eth.personal.unlockAccount(user_cred.username, user_cred.password, 600);
	// Storing energy consumption readings
	consumers_storage.methods.addDataEntry(parseInt(current_timestamp), parseInt(voltage_value), parseInt(power_value), parseInt(energy_value)).send({from: user_cred.username, gas: 150000})
}, 900000);

