Currently WIP and will be completed soon.

# Shelly-Automated-Agile-Octopus
An open-source system of scripts that can be used to automate a Shelly relay to switch on during the cheapest period of your Agile Octopus tariff.

## Features
- Calculates the cheapest period of electricity prices per day.
- Switches on a Shelly relay with the cloud during the cheapest period, then switches it off outside of that period.
- Uses an interface which runs on the local network to display Agile Octopus' half-hourly prices and control the system.

## Hardware List


|Devices|Source|
---------|------
|Raspberry Pi 4b| https://thepihut.com/products/raspberry-pi-4-model-b?src=raspberrypi&variant=20064052674622|
|Shelly 1pm| https://shellystore.co.uk/product/shelly-1pm-gen3/|
|GME12864-43 30pins Display| https://www.alibaba.com/product-detail/New-Design-GME12864-43-30pins-Yellow_1600294817612.html|


|Power/Connectors|Source|
-----|-----
|Rapsberry Pi 15W USB-C Power Supply|https://thepihut.com/products/raspberry-pi-4-model-b?variant=20064052674622|
|14 AWG or 2.5mm<sup>2</sup> Wire|https://www.amazon.co.uk/dp/B0CZRGZTLZ?ref=ppx_yo2ov_dt_b_fed_asin_title|
|Jumper Wires|https://www.amazon.co.uk/dp/B074P726ZR?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1|


If you would like to house the Shelly relay in its own enclosure instead of connecting it to a pre-installed electrical socket, here's some hardware that can be used to create a home-made smartplug, essentially.

|Power/Connectors for the Relay Enclosure|Source|
----|-----
|C14 Panel Mount IEC Connector Male|https://uk.rs-online.com/web/p/iec-connectors/0488191?gb=s|
|IEC C13 Socket to Type G UK Plug Power Cord|https://uk.rs-online.com/web/p/power-cords/2621126?gb=s|
|UK Switched Electrical Socket|https://www.amazon.co.uk/dp/B01L4P5LVC?ref=ppx_yo2ov_dt_b_fed_asin_title|




*Note: The exact hardware used for the system were listed, but other devices can be used. For example, the Raspberry Pi 4b can be substituted for the cheaper Pi Zero 2W variant. One thing to consider, at the moment, .stl models to house the system are only available for the listed parts.*





