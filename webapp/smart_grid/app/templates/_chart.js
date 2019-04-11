// Initialize chart object
yValues = [];
{% if subdomain == '' %}
unit = 'kW';
decimalPoints = 2;
{% else %}
unit = 'MW';
decimalPoints = 0;
{% endif %}
{% if url_for(request.endpoint)[1:] in ['set_tariff'] %}
{% for key in consumption_tariff %}
	yValues.push({{ consumption_tariff[key] }});
{% endfor %}
axisYFormat = {
	title: "Energy Tariff (¢)",
	interval: 0.2,
	minimum: Math.min.apply(null, yValues) - 0.5,
	maximum: Math.max.apply(null, yValues) + 0.5
};
{% elif url_for(request.endpoint)[1:] in ['set_incentive'] %}
{% for key in incentive %}
	yValues.push({{ incentive[key] }});
{% endfor %}
axisYFormat = {
	title: "Incentive (¢)",
	interval: 0.5,
	minimum: Math.min.apply(null, yValues) - 0.5,
	maximum: Math.max.apply(null, yValues) + 0.5
};
{% elif url_for(request.endpoint)[1:] in ['set_limit', 'home'] %}
{% for key in data_entries %}
	yValues.push({{ data_entries[key] }});
{% endfor %}
{% for key in prediction %}
	yValues.push({{ prediction[key] }});
{% endfor %}
{% if subdomain == '' %}
minFormat = null;
{% else %}
minFormat = Math.floor(Math.min.apply(null, yValues) / 1000) * 1000 - 250;
{% endif %}
axisYFormat = {
	title: `Energy Consumption (${unit})`,
	minimum: minFormat
};
{% endif %}
var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	axisX: {
		interval: 1,
		intervalType: "hour",
		valueFormatString: "HH:mm"
	},
	axisY: axisYFormat,
	data: [{
		type: "line",
		markerType: marker_type,
		dataPoints: data_entries
	}]
});
// Add prediction data to chart for set_limit page
{% if url_for(request.endpoint)[1:] in ['set_limit'] or (subdomain != '' and url_for(request.endpoint)[1:] in ['home']) %}
chart.options.data.push({
	type: "line",
	markerType: "none",
	dataPoints: prediction_data
})
{% endif %}

{% if url_for(request.endpoint)[1:] in ['set_limit', 'set_tariff', 'set_incentive'] %}
// Show tooltip for cost and incentive information
chart.options.toolTip = {
	shared: true,
	contentFormatter: function(e) {
		// Get current time
		var xValue = e.entries[0].dataPoint.x
		// Get consumption
		{% if url_for(request.endpoint)[1:] in ['set_limit'] %}
		var contentRealConsumption = "Energy Consumption Limit: " + e.entries[0].dataPoint.y.toFixed(decimalPoints) + " " + unit;
		{% endif %}
		var contentPrediction = "Predicted Energy Consumption: " + {{ prediction }}[xValue.getTime() / 1000].toFixed(decimalPoints) + " " + unit;
		// Calculate offset
		var xTimestamp = xValue.getTime() / 1000
		var today = new Date()
		var timestampToday = (new Date(today.getFullYear(), today.getMonth(), today.getDate())).getTime() / 1000
		var timeOffset = (xTimestamp - timestampToday) / 1800
		var contentTime = xValue.toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'});
		{% if url_for(request.endpoint)[1:] in ['set_tariff'] %}
		var contentTariff = "Tariff: ¢" + e.entries[0].dataPoint.y;
		{% else %}
		var contentTariff = "Tariff: ¢" + {{ consumption_tariff }}[timeOffset];
		{% endif %}
		{% if url_for(request.endpoint)[1:] in ['set_incentive'] %}
		var contentIncentive = ((e.entries[0].dataPoint.y < 0) ? "Incentive: -¢" : "Incentive: ¢") + Math.abs(e.entries[0].dataPoint.y);
		{% else %}
		var contentIncentive = (({{ incentive }}[timeOffset] < 0) ? "Incentive: -¢" : "Incentive: ¢") + Math.abs({{ incentive }}[timeOffset]);
		{% endif %}
		{% if url_for(request.endpoint)[1:] in ['set_limit'] %}
		var content = "<div style='width:100%; text-align:center;'><strong>" + contentTime + "</strong></div>" + contentRealConsumption + "<br>" + contentPrediction + "<br><br>" + contentTariff + "<br>" + contentIncentive;
		{% else %}
		var content = "<div style='width:100%; text-align:center;'><strong>" + contentTime + "</strong></div>" + contentPrediction + "<br><br>" + contentTariff + "<br>" + contentIncentive;
		{% endif %}
		return content;
	}
};
{% endif %}

{% if url_for(request.endpoint)[1:] in ['home'] %}
chart.options.toolTip = {
	shared: true,
	contentFormatter: function(e) {
		var xValue = e.entries[0].dataPoint.x;
		var contentTime = xValue.toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'});
		{% if subdomain == '' %}
		var contentRealConsumption = "Real-Time Energy Consumption: " + ((e.entries[0].dataPoint.y != null) ? (e.entries[0].dataPoint.y.toFixed(decimalPoints) + " " + unit) : ' -');
		{% else %}
		var contentRealConsumption = "Predicted Energy Consumption: " + e.entries[0].dataPoint.y.toFixed(decimalPoints) + " " + unit;
		{% endif %}
		var content = "<div style='width:100%; text-align:center;'><strong>" + contentTime + "</strong></div>" + contentRealConsumption;
		if (e.entries[1] != null) {
			var contentPrediction = "Predicted Energy Consumption: " + e.entries[1].dataPoint.y.toFixed(decimalPoints) + " " + unit;
			content += "<br>" + contentPrediction;
		}
		return content;
	}
};
{% endif %}
chart.render();

// Declare variables for draggable chart
var xSnapDistance = 300000;
var ySnapDistance = 3;
var xValue, yValue;
var maxY = Math.max.apply(null, yValues);
var minY = Math.min.apply(null, yValues);
var mouseDown = false;
var dblClick = false;
var selected = null;
var changeCursor = false;
var timerId = null;

// Get position of cursor in terms of values of the chart
function getPosition(e) {
	var parentOffset = $('#chartContainer > .canvasjs-chart-container').offset();

	var relX = e.pageX - parentOffset.left;
	var relY = e.pageY - parentOffset.top;
	xValue = Math.round(chart.axisX[0].convertPixelToValue(relX));
	{% if url_for(request.endpoint)[1:] in ['set_tariff', 'set_incentive', 'set_limit'] %}
	yValue = Math.round(chart.axisY[0].convertPixelToValue(relY) * 100) / 100;
	{% else %}
	yValue = Math.round(chart.axisY[0].convertPixelToValue(relY));
	{% endif %}
}

// Search corresponding data point based on cursor location
function searchDataPoint() {
	var dps = chart.data[0].dataPoints;
	for (var i = 0; i < dps.length; i++) {
		if ((xValue >= dps[i].x.getTime() - xSnapDistance && xValue <= dps[i].x.getTime() + xSnapDistance) && (yValue >= dps[i].y - ySnapDistance && yValue <= dps[i].y + ySnapDistance)) {
			if (mouseDown || dblClick) {
				selected = i;
				break;
			} else {
				changeCursor = true;
				break;
			}
		} else {
			selected = null;
			changeCursor = false;
		}
	}
}

function setDataPoint() {
	yValue = Number(document.getElementById('new-value').value);
	{% if url_for(request.endpoint)[1:] in ['set_limit'] %}
	refreshCosts(calculatePredictedCost(), calculateCurrentCost(), calculateCostSavings());
	{% endif %}
	if (yValue >= 0 || {{ 'true' if subdomain == 'government' else 'false' }}){
		chart.data[0].dataPoints[selected].y = yValue;
	} else {
		chart.data[0].dataPoints[selected].y = 0;
	}
	if (yValue < minY) {
		axisYFormat.minimum = yValue - 0.5;
		minY = yValue;
	} else if (yValue > maxY) {
		axisYFormat.maximum = yValue + 0.5;
		maxY = yValue;
	}
	chart.options.axisY = axisYFormat;
	chart.render();
	dblClick = false;
}