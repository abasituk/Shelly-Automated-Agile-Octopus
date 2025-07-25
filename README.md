# Shelly-Automated-Agile-Octopus
A system of scripts that can be used to automate a Shelly relay to switch on during the cheapest period of your Agile Octopus tariff. The relay will then switch off outside of that period.


![System Diagram (1)](https://github.com/user-attachments/assets/044ee987-41b2-41e3-8bf1-6798a16e9012)

Any python capable device with WiFi should be able to run this system. A Raspberry Pi 4B is used for the build tutorial.



## Function
- Calculates the cheapest period of electricity prices per day.
- Switches on a Shelly relay through the cloud during the cheapest period, then switches it off outside of that period.
- Hosts a webpage which runs on the local network to display Agile Octopus' half-hourly prices and control the system.

# Hardware List

|Count|Devices|Source|
------|---|------
1|Raspberry Pi 4b| [ThePiHut](https://thepihut.com/products/raspberry-pi-4-model-b?src=raspberrypi&variant=20064052674622)|
1|Shelly 1PM Gen3| [ShellyStore](https://shellystore.co.uk/product/shelly-1pm-gen3/)|
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
1|IEC C13 Socket to Type G UK Plug Power Cord|[ThePiHut](https://thepihut.com/products/kettle-type-power-cable-2m-iec-c13-uk)|
1|UK Switched Electrical Socket (2 poles)|[RS-Electronics](https://uk.rs-online.com/web/p/plug-sockets/2227904?gb=s)|
6|M3 x 8 length Bolts|
6|M3 Nuts|
2|M4 Screws|
2|M4 Nuts|
3|Spade Connectors/quick disconnect connectors unless soldering|

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

1. The display can be connected to the Raspberry Pi with jumper wires according to the schematic:

|Display|Raspberry Pi Pin|Raspberry Pi Pin Name|
|-|-|-|
SDA|3|GPIO2
SCL|5|GPIO3
VCC|1|3V3
GND|9|GND

![Controller Circuit](https://github.com/user-attachments/assets/1dc16f84-1673-4b1d-b6df-e4ffe167df4c)

2. The Raspberry Pi can then be mounted to the floor of the enclosure with 4 M3 bolts, and the screen to the side of the enclosure with M3 bolts and nuts:

![image](https://github.com/user-attachments/assets/49a66935-6fbc-4d1d-9047-b8bfea63cb76)


## Relay Subsystem Build Guide

*Assuming you are creating a DIY smartplug with the Shelly relay and not wiring it to a pre-existing electrical socket.*

1. The Shelly 1PM gen3 can be wired to the C14 Panel Mount IEC connector according to the schematic provided in its manual:

![Shelly 1PM gen3 Fig 1 Whitebg](https://github.com/user-attachments/assets/76067b43-84bf-42d2-a14c-8e51e325dce8)

|Shelly|IEC Connector|
------|-----------
|N|Neutral
|L|Live

2. An L terminal from the Shelly is then connected to its own SW terminal.
3. The Shelly's 0 Terminal can then be connected to the electrical socket's live, and the Shelly's remaining N terminal to the socket's neutral.
4. The ground from the IEC connector can then be connected to the electrical socket's ground.
5. After the wiring is complete, the Shelly relay can be constrained with a ziptie, and the socket can be screwed into the enclosure.

![Relay Wiring Gif 4](https://github.com/user-attachments/assets/ce56dd81-7b71-425b-a129-cec5dee47a9d)


<details>
  <summary>Individual Relay Wiring Images</summary>
  <img src="https://github.com/user-attachments/assets/e54d1276-c58b-4927-a801-2635ffa3e9bc" alt="image-description"/>
  <img src="https://github.com/user-attachments/assets/29cf12f8-a353-468a-b2dd-ce19f07cf2cc" alt="image-description"/>
  <img src="https://github.com/user-attachments/assets/abffacfd-6fce-4db6-b39a-2415d288a5a0" alt="image-description"/>
  <img src="https://github.com/user-attachments/assets/c59d87ee-dca3-40d6-9a51-95a95ff259a5" alt="image-description"/>
  <img src="https://github.com/user-attachments/assets/b5427da0-1dbc-4c3c-b86a-868e534408a8" alt="image-description"/>
  <img src="https://github.com/user-attachments/assets/4a676f61-9362-4749-9d53-0225243fc83d" alt="image-description"/>
  <img src="https://github.com/user-attachments/assets/7df5679c-3656-4469-86dc-8f61b9b801cf" alt="image-description"/>
</details>



# installation guide

## Initial Raspberry Pi Setup

1. Using [Raspberry Pi Imager](https://www.raspberrypi.com/software/), select your Raspberry Pi model, Raspberry Pi OS (64 bit) and your microSD card, then press next
   
![Imager 1](https://github.com/user-attachments/assets/66c077a2-c61e-4ebd-8514-226a35b4692d)

2. On the dialogue that pops up, edit the custom OS settings to allow your Pi to connect to your WiFi

![Imager 2](https://github.com/user-attachments/assets/638a2733-6d52-4e4e-9ef6-1e11743e6b82)

3. Type in a username and password for your Pi, then your WiFi name and password
  
![Imager 3](https://github.com/user-attachments/assets/3ed3baec-953b-4fa3-a4a1-2d5e36912d0e)

4. Save and apply the settings, then write to your microSD card

5. Find your Pi's IP address (this can be found in your router connections), then SSH into your Pi. [PuTTy](https://www.putty.org) is an open source software commonly used for this.
(Type in your Pi's IP address and click open.)

![image](https://github.com/user-attachments/assets/2cacee12-fb02-4873-ac17-772a020593d5)

6. Type in your Pi's username and password


## System Installation

*Here you can type these commands into your terminal to easily setup the system*

1. Download install.sh
```
wget https://raw.githubusercontent.com/abasituk/Shelly-Automated-Agile-Octopus/main/Install.sh
```

2. Give it permission to run
```
chmod +x Install.sh
```

3. Run it with sudo, the script will download the scripts, services and requirements
```
sudo ./Install.sh
```

<br/>

4. After the installation is finished, enable your I2c Interface by first opening your config

  4a. Open your Pi's config
```
sudo raspi-config
```

4b. Open 'Interface Options'

![image](https://github.com/user-attachments/assets/d0306fa2-bd10-4aa8-91ff-fabdbdd94460)

4c. Select 'I2C'

![image](https://github.com/user-attachments/assets/233ba3a7-eef2-45eb-bcdd-09ff6982c3b1)

4d. Enable the I2C interface

![image](https://github.com/user-attachments/assets/adf2fdbe-d6f4-4a4d-8eb6-d6021f85b050)

4e. Use your right arrow key to select <Finish> and press enter

![image](https://github.com/user-attachments/assets/3651227b-5b3e-4ff8-ae08-23c5ad4e5c2c)

<br/>
5. Add your Shelly and tariff details to the system's config.ini file
5a. Navigate to where the system was installed

```
cd /home/pi/shelly
```

5b. Open config.ini
```
nano config.ini
```

5c. Add your Shelly and tariff details to the config.ini file without the comments:
```
[Shelly_Variables]                         # Available at https://control.shelly.cloud/
DEVICE_ID = X                                  # device settings -> Device information
SERVER_URI = shelly-X-eu.shelly.cloud          # account settings -> Authorization cloud key (note: not including https://)
AUTH_KEY = X                                   # account settings -> Authorization cloud key

[Tariff_Details]                       # Details for your agile octopus tariff (to interact with the API)
region_code = B                          # Region code for east midlands (e.g. Lincolnshire)
product_code = AGILE-24-10-01            # Your agile octopus tariff's product code
electricity_tariff_type = E-1R           # As Agile Octopus prices change based on wholesale prices, this probably won't need changing
period_size = 1                          # How long you would like your appliance to be switched on (1 period = 0.5 hours)

[Timing_Variables]                     # How quickly the code will loop
INTERVAL = 2                             # Determines how quickly the webgraph updates, increase the value if your Pi is struggling
```

5d. Once the details have been added, press `Ctrl+X`, then `Y`, then `Enter` to save and exit the config.ini file.

<br/>

6. Reload Systemd
```
sudo systemctl daemon-reload
```

7. Restart your services
```
sudo systemctl restart shellycontrol.service webgraph.service
```

<br/>

After these steps, you should be able to type `http://'Your Pi's IP Address':8080` into a browser on the same WiFi network and see your Pi's webgraph.

You can also check the status of the services to see if there are any errors (press `Ctrl+C` to exit the status):
```
systemctl status shellycontrol.service
```
and
```
systemctl status webgraph.service
```





