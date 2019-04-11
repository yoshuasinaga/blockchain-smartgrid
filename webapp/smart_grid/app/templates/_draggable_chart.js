document.getElementById('set-value-btn').addEventListener('click', setDataPoint);
document.getElementById('set-value-form').addEventListener('keydown', function(e) {
	if (e.keyCode == 13) {
		e.preventDefault();
		document.getElementById('set-value-btn').click();
		return false;
	}
})

// Event listeners for draggable chart
jQuery("#chartContainer > .canvasjs-chart-container").on({
	dblclick: function(e) {
		console.log("Double Clicked!");
		dblClick = true;
		getPosition(e);
		searchDataPoint();
		if (selected != null) {
			document.getElementById('new-value').value = null;
			promptSetValue();
		}
	},
	mousedown: function(e) {
		mouseDown = true;
		getPosition(e);
		searchDataPoint();
	},
	mousemove: function(e) {
		getPosition(e);
		if (mouseDown) {
			clearTimeout(timerId);
			timerId = setTimeout(function() {
				if (selected != null) {
					if (yValue >= 0 || {{ 'true' if subdomain == 'government' else 'false' }}) {
						chart.data[0].dataPoints[selected].y = yValue;
						{% if url_for(request.endpoint)[1:] in ['set_tariff', 'set_incentive'] %}
						if (yValue < minY) {
							axisYFormat.minimum = yValue - 0.5;
						} else if (yValue > maxY) {
							axisYFormat.maximum = yValue + 0.5;
						}
						chart.options.axisY = axisYFormat;
						{% endif %}
					} else {
						chart.data[0].dataPoints[selected].y = 0;
						axisYFormat.minimum = -1;
						jQuery("#chartContainer > .canvasjs-chart-container").mouseup();
					}
					chart.render();
				}
			}, 0);
		} else {
			searchDataPoint();
			if (changeCursor) {
				chart.data[0].set("cursor", "n-resize");
			} else {
				chart.data[0].set("cursor", "default");
			}
		}
	},
	mouseup: function(e) {
		console.log('mouseup');
		if (selected != null) {
			{% if url_for(request.endpoint)[1:] in ['set_limit'] %}
			refreshCosts(calculatePredictedCost(), calculateCurrentCost(), calculateCostSavings());
			{% endif %}
			if (yValue >= 0 || {{ 'true' if subdomain == 'government' else 'false' }}){
				chart.data[0].dataPoints[selected].y = yValue;
			} else {
				chart.data[0].dataPoints[selected].y = 0;
			}
			if (yValue < minY) {
				minY = yValue;
			} else if (yValue > maxY) {
				maxY = yValue;
			}
			chart.render();
			mouseDown = false;
		}
	}
});