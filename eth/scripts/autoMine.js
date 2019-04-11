var mining_threads = 1

function checkTxn() {
	if (eth.getBlock('pending').transactions.length > 0) {
		if (eth.mining) return;
		console.log('== Pending transactions available! Mining...');
		miner.start(mining_threads);
	} else {
		if (eth.mining) {
			console.log('== No pending transactions available! Mining stopped.');	
		}
		miner.stop();
	}
}

eth.filter("latest", function(err, block) {
	checkTxn();
});

eth.filter("pending", function(err, block) {
	checkTxn();
});

checkTxn();