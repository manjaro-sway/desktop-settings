# Manjaro Openbox

## Configuable
Openbox is highly configurable and there is virtually no limits on what you can do.

## Elementary
### Keyboard shortcuts AKA keybinds
The configuration of Openbox has a lot of keyboard shortcuts - it is not possible to explain them all - just say - most of them is working with window navigation, tiling and moving windows.

To mention two tiling shortcuts

* <kbd>Alt</kbd><kbd>Numpad 1 to 9</kbd> tile active window to a fourth
* <kbd>Win</kbd><kbd>Numpad 1 to 9</kbd> tile active window to a sixth

### Available keybinds
To list all keybinds open the desktop menu and navigate to **Shortcuts**.

### Changing preferences
All settings can be found in the desktop root menu **Preferences**.

### Dynamic desktop menu
This configuration of Openbox is using a static root menu including a dynamic Application menu. Should you prefer you can switch to a dynamic menu using the **Switch Menu** item.

### Polybar or Tint2 or both
Should you prefer Tint2 over Polybar it is easy to change from the **Settings and Preferences** root menu. Remember to edit the Openbox **autostart** file and enable Tint2.

### $HOME/openbox/autostart
The file contains several options which you enable/disable according to preference

### Polybar is configured using modules
Having them all in one file is confusing so they are split out to their own files in `~/.config/polybar/modules`. Some modules are just examples and not configured identical.

To include a module modify the configuration in the main config folder

* uncomment the module in `modules.conf`
* add it to the configuration in `config` found

### Compositor
Compton has been renamed to picom and as such the configuration has been moved to `$HOME/.config/picom/picom.conf`.

Compositing may behave differently for different hardware combination. The defaults in the configuration is on a best effort base - you may need to adjust.

Especially if you are using Nvidia graphics - it may be a better solution to use the Nvidia compositor.

### Help and Info
All kinds of help and info are available from the desktop menu **Help and Info**

## Network address display
Conky and Polybar needs information of your network interfaces if you want the IP address displayed.

For the users of VPN services both polybar an conky displays your current wan ip. If you are disconnected from VPN you will quickly notice.

### Conky network
Conky can be controlled using the **Conky Chooser** from the **Preferences** menu.

Conky files is the new lua format and placed in your home's **.config/conky** folder.

To make your IP address appear in the conky you need to set the correct interface names.

    nmcli | grep -e en -e wl

Then insert the interface names in the **template1** and **template2** and save the file

    -- ethernet
        template1 = 'eth0',
    -- wireless
        template2 = 'wlan0',

### Polybar network
Edit the file `~/.config/polybar/config` and insert the interface names and save file. When the `config` file is saved polybar should reload. If not choose the **Restart Polybar** from the desktop menu **Preference** &rarr; **Restart Polybar**.

    ;=====================================================
    ;     Network interfaces
    ;=====================================================
    ; use nmcli to list your devices - restart polybar
    ; nmcli | grep -e en -e wl
    [nic]
    lan = $ETHERNET
    wlan = $WIFI

## Conky Weather info

To change the displayed weather location edit the conky config and change the **template0** to print the desired text

    -- location
        template0 = 'LINUX AARHUS',

To actual display your locations weather info - open the [AccuWeather.com][1] webpage and locate your city.

When you have your city's weather forecast in your browser - goto the source of the page and locate the javascript variable named

    var currentLocation =

This variable hold the data needed for the rss link - which is parsed by acc_rss script. The below codeblock is the datastructure for the city of Aarhus in Denmark.

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


From the datastructure you need the following values

    currentLocation.region.id = EUR
    currentLocation.country.id = DK
    currentLocation.key = 124594
    currentLocation.localizedName = AARHUS


Edit the file `~/.config/conky/accu_weather/acc_rss` and insert the values from the data structre

	# PUT YOUR LOCATIONS PARAMETERS IN THE VARIABLES BELOW
	REGION_ID="EUR"
	COUNTRY_ID="DK"
	LOCATION_KEY="124594"
	LOCALIZED_NAME="AARHUS"


[1]: https://www.accuweather.com
