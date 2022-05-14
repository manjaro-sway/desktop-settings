## Weather location

Open [AccuWeather.com][1] and locate your city.

When you have your city's weather forecast in your browser - goto the source of the page and locate the javascript variable named

    var currentLocation =

This variable hold the data need for the rss link which is parsed by acc_rss script. The below codeblock is the datastructure for the city of Aarhus in Denmark.

	var currentLocation = {
		"administrativeArea":{
			"englishName":"Central Jutland",
			"id":"82",
			"localizedName":"Midtjylland"
		},
		"country":{
			"englishName":"Denmark",
			"id":"DK",
			"localizedName":"Danmark"
		},
		"englishName":"Aarhus",
		"gmtOffset":1.0,
		"timeZoneCode":"CET",
		"hasAlerts":true,
		"hasForecastConfidence":true,
		"hasMinuteCast":true,
		"hasRadar":true,
		"key":"124594",
		"lat":56.155,
		"localizedName":"Aarhus",
		"lon":10.173,
		"primaryPostalCode":"",
		"region":{
			"englishName":"Europe",
			"id":"EUR",
			"localizedName":"Europa"
		},
		"timeZone":"CET"
	};


From the datastructure you need the following data in the mentioned order

The value of

    currentLocation.region.id = EUR
    currentLocation.country.id = DK
    currentLocation.key = 124594
    currentLocation.localizedName = AARHUS


Edit the file acc_rss and insert the values from the data structre

	# PUT YOUR LOCATIONS PARAMETERS IN THE VARIABLES BELOW
	REGION_ID="EUR"
	COUNTRY_ID="DK"
	LOCATION_KEY="124594"
	LOCALIZED_NAME="AARHUS"


[1]: https://www.accuweather.com