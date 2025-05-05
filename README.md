Currently WIP and will be completed soon.

# Shelly-Automated-Agile-Octopus
An open-source system of scripts that can be used to automate a Shelly relay to switch on during the cheapest period of your Agile Octopus tariff.

## Function
- Calculates the cheapest period of electricity prices per day.
- Switches on a Shelly relay with the cloud during the cheapest period, then switches it off outside of that period.
- Hosts a webpage which runs on the local network to display Agile Octopus' half-hourly prices and control the system.

# Hardware List

|Devices|Source|
---------|------
|Raspberry Pi 4b| https://thepihut.com/products/raspberry-pi-4-model-b?src=raspberrypi&variant=20064052674622|
|Shelly 1pm| https://shellystore.co.uk/product/shelly-1pm-gen3/|
|GME12864-43 30pins Display| https://www.alibaba.com/product-detail/New-Design-GME12864-43-30pins-Yellow_1600294817612.html|

|Power/Connectors|Source|
-----|-----
|Rapsberry Pi 15W USB-C Power Supply|[ThePiHut](https://thepihut.com/products/raspberry-pi-4-model-b?variant=20064052674622)|
|14 AWG or 2.5mm<sup>2</sup> Wire|[Amazon](https://www.amazon.co.uk/dp/B0CZRGZTLZ?ref=ppx_yo2ov_dt_b_fed_asin_title)|
|Jumper Wires|[Amazon](https://www.amazon.co.uk/dp/B074P726ZR?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1)|


If you would like to house the Shelly relay in its own enclosure instead of connecting it to a pre-installed electrical socket, here's some hardware that can essentially be used to create a smartplug with it

|Power/Connectors for the Relay Enclosure|Source|
----|-----
|C14 Panel Mount IEC Connector Male|[RS-Electronics](https://uk.rs-online.com/web/p/iec-connectors/0488191?gb=s)|
|IEC C13 Socket to Type G UK Plug Power Cord|[RS-Electronics](https://uk.rs-online.com/web/p/power-cords/2621126?gb=s)|
|UK Switched Electrical Socket|[Amazon](https://www.amazon.co.uk/dp/B01L4P5LVC?ref=ppx_yo2ov_dt_b_fed_asin_title)|

If an automated smartplug is more desirable, substituting the Shelly relay for a [Shelly smartplug](https://shellystore.co.uk/product/shelly-plus-plug-uk/) could be easier and more cost-effective, but the WiFi capable model appears to have been out of stock for atleast a few months. Due to this, it has not yet been tested to see if it could work with the current code provided.

*Note: The exact hardware used for the system were listed, but some alternative devices can be used. For example, the Raspberry Pi 4b can be substituted for the cheaper, more compact Pi Zero 2W variant. One thing to consider, is that at the moment, the .stl models to house the system are only available for the listed parts.*

