Currently WIP and will be completed soon.

# Shelly-Automated-Agile-Octopus
An open-source system of scripts that can be used to automate a Shelly relay to switch on during the cheapest period of your Agile Octopus tariff.

## Function
- Calculates the cheapest period of electricity prices per day.
- Switches on a Shelly relay with the cloud during the cheapest period, then switches it off outside of that period.
- Hosts a webpage which runs on the local network to display Agile Octopus' half-hourly prices and control the system.

# Hardware List

|Count|Devices|Source|
------|---|------
1|Raspberry Pi 4b| [ThePiHut](https://thepihut.com/products/raspberry-pi-4-model-b?src=raspberrypi&variant=20064052674622)|
1|Shelly 1pm| [ShellyStore](https://shellystore.co.uk/product/shelly-1pm-gen3/)|
1|GME12864-43 30pins Display| [ThePiHut](https://thepihut.com/products/0-96-oled-display-module-128x64)|

Count|Power/Connectors|Source|
-----|-|----
1|Rapsberry Pi 15W USB-C Power Supply|[ThePiHut](https://thepihut.com/products/raspberry-pi-4-model-b?variant=20064052674622)|
1|14 AWG or 2.5mm<sup>2</sup> Wire|[Amazon](https://www.amazon.co.uk/dp/B0CZRGZTLZ?ref=ppx_yo2ov_dt_b_fed_asin_title)|
4|Jumper Wires|[Amazon](https://www.amazon.co.uk/dp/B074P726ZR?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1)|
8|M3 x 8 length Bolts|



If you would like to house the Shelly relay in its own enclosure instead of connecting it to a pre-installed electrical socket, here's some hardware that can essentially be used to create a smartplug with it

Count|Power/Connectors for the Relay Enclosure|Source|
--|--|-----
1|C14 Panel Mount IEC Connector Male|[RS-Electronics](https://uk.rs-online.com/web/p/iec-connectors/0488191?gb=s)|
1|IEC C13 Socket to Type G UK Plug Power Cord|[RS-Electronics](https://uk.rs-online.com/web/p/power-cords/2621126?gb=s)|
1|UK Switched Electrical Socket|[Amazon](https://www.amazon.co.uk/dp/B01L4P5LVC?ref=ppx_yo2ov_dt_b_fed_asin_title)|
4|M3 x 8 length Bolts|
2|M3 Nuts|

For an automated smartplug, substituting the Shelly relay for a [Shelly smartplug](https://shellystore.co.uk/product/shelly-plus-plug-uk/) may be more straightforward and cost-effective, but the WiFi capable model appears to have been out of stock for atleast a few months. Due to this, it has not yet been tested whether it could work with the current code provided.

*Note: The exact hardware used for the system were listed, but some alternative devices can be used. For example, the Raspberry Pi 4b can be substituted for the cheaper, more compact Pi Zero 2W variant. One thing to consider though, is that at the moment, the .stl models to house the system are only available for the listed parts.*


# Hardware Build Guide

This section describes how to build two subsystems:
- The Control Subsystem:
  - Consists of the Raspberry Pi and display, calculates the cheapest period of energy prices and controls the relay.
- The Relay Subsystem:
  - A DIY smartplug which consists of the Shelly relay and connects to an appliance to switch it on or off.

*Enclosures are available to be 3D printed for each subsystem, but are not strictly necessary.*

## Control Subsystem Build Guide

The display can be connected to the Raspberry Pi with jumper wires according to the schematic
![image](https://github.com/user-attachments/assets/d0292c35-3625-4f94-b28f-73a349830ea5)


