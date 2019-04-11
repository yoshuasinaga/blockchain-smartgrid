from web3 import Web3
from config import Config

import json
import os

# Contract name to be in CONTRACT_NAME
def get_smart_contract(w3, contract_name):
	abi = json.loads(Config.ABI[contract_name])
	return w3.eth.contract(abi=abi, address=Web3.toChecksumAddress(Config.CONTRACT_ADDR[contract_name]))
