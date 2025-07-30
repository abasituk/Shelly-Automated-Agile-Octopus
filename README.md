# Shelly-Automated-Agile-Octopus
A system used to automate a Shelly relay to switch on during the cheapest period of the Agile Octopus tariff.


![System Diagram (1)](https://github.com/user-attachments/assets/044ee987-41b2-41e3-8bf1-6798a16e9012)

The software requires a Python capable device with WiFi. A Raspberry Pi 4B is used for the build tutorial, with alterantives including cheaper models, such as the Pi Zero 2 W.



## System Functions
- Calculates the cheapest period of electricity prices per day.
- Switches on a Shelly relay through the cloud during the cheapest period, then switches it off outside of that period.
- Hosts a webpage which runs on the local network to display Agile Octopus' half-hourly prices and control the system.

# Hardware List

The relay subsystem may use a Shelly relay when installed into an existing socket or a Shelly Plus plug for portability.



### 1a. BOM for the IoT-based system (Configuration 1).

| Identifier | Component | Quantity | Component Cost [GBP] | Source |
|---|---|---|---|---|
| SBC | Raspberry Pi Zero 2W | 1 | £16.98 | ThePiHut |
| Display | 0.96" OLED Display Module | 1 | £4.00 | ThePiHut |
| SBC Power | Raspberry Pi 12.5W Power Supply | 1 | £7.50 | ThePiHut |
| Smart Relay | Shelly 1PM Gen3 | 1 | £18.50 | ThePiHut |

### 1b. Alternative BOM for the IoT-based system, utilising a smart plug (Configuration 2).

| Identifier | Component | Quantity | Component Cost [GBP] | Source |
|---|---|---|---|---|
| SBC | Raspberry Pi Zero 2W | 1 | £16.98 | ThePiHut |
| Display | 0.96" OLED Display Module | 1 | £4.00 | ThePiHut |
| SBC Power | Raspberry Pi 12.5W Power Supply | 1 | £7.50 | ThePiHut |
| Smart Relay | Shelly Plus Plug | 1 | £18.50 | ThePiHut |

### 3. Additional components used for the control subsystems assembly.

Count|Power/Connectors|
-----|----------------|
1|Rapsberry Pi 15W USB-C Power Supply|
1|14 AWG or 2.5mm<sup>2</sup> Wire|
4|Jumper Wires|
4|M3 x 8 Bolts|
4|M3 Nuts
4|M2 x 6 Bolts|
4|M2 Nuts

If the Shelly Plus plug is be unavailable for purchase, the Shelly relay can be utilised in a customised portable relay subsystem.
### 4. Optional components used to build a portable relay subsystem with the Shelly Relay.

Count|Component
--|--
1|C14 Panel Mount IEC Connector Male
1|IEC C13 Socket to Type G UK Plug Power Cord
1|UK Switched Electrical Socket (2 poles)
6|M3 x 8 length Bolts
6|M3 Nuts
2|M4 Screws
2|M4 Nuts
3|Spade/quick disconnect connectors




# Hardware Build Guide

This section describes how to build two subsystems:
- The Control Subsystem:
  - Consisting of the Raspberry Pi and display, it calculates the cheapest period of energy prices and controls the relay.
- The Relay Subsystem:
  - A circuit which utilises a relay to power an appliance as requested by the control subsystem.


## Control Subsystem Build Guide

### Control Subsystem Printing List

| Count | Model                                    |
|-------|------------------------------------------|
| 1     | Pi Zero 2W Enclosure With Screen.stl     |
| 2     | Pi Zero 2W Enclosure With Screen Cap.stl |


1. The display is connected to the Raspberry Pi with jumper wires.

|Display|Raspberry Pi Pin|Raspberry Pi Pin Name|
|-|-|-|
SDA|3|GPIO2
SCL|5|GPIO3
VCC|1|3V3
GND|9|GND


2. The Raspberry Pi and display are mounted to the floor of the enclosure with 4 M3 bolts and M2 bolts.

<img width="709" height="335" alt="image" src="https://github.com/user-attachments/assets/04671383-743e-4d19-8aff-ed5de0c9f266" />

3. The enclosure is folded along its live hinges.

4. Endcaps are press-fitted to both ends.

## Relay Subsystem Build Guide

*Outlines the installation of the Shelly relay into an electrical socket*


1. The Shelly 1PM gen3 is wired according to the diagram:

<img width="400" alt="image" src="https://github.com/user-attachments/assets/18c5dd80-a536-444d-8b5b-b3028d5502b9" />

<img src="https://github.com/user-attachments/assets/ce56dd81-7b71-425b-a129-cec5dee47a9d" width="400">

An animation displays this process, where power is delivered through an IEC connector.


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

## Raspberry Pi Setup

1. Using [Raspberry Pi Imager](https://www.raspberrypi.com/software/), select the utilised Raspberry Pi model, Raspberry Pi OS (64 bit) and your microSD card, then press next

2. On the dialogue that appears, edit the custom OS settings to allow your Pi to connect to your WiFi

3. Type in a username and password for your Pi, then your WiFi name and password

4. Save and apply the settings, then write to your microSD card

5. SSH into the Pi.



## System Installation

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

4c. Select 'I2C'

4d. Enable the I2C interface

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
