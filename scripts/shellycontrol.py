import requests
import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
from adafruit_ssd1306 import SSD1306_I2C
from datetime import datetime

# Variables =======================================================================================
# Typed in camelCase just for ease of distinguishing them in the code
interval = 0.1 # How quick the script is looped
webpageURL = "http://localhost:8080" # this is localhost as the webpage is hosted on the same device

# Set up the OLED screen by setting the pins used
# adafruit_ssd1306 is used because it is compatible with the OLED display
pins = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, pins)

# Set up the display to not have to refresh fully to display something new,
# instead only the pixels that change need to be refreshed, 
# this reduces the screen flashing on and off
previous_display = {
    "optimal_period": "",
    "currently_optimal": "",
    "auto_mode": "",
    "relay_status": ""
}



# Functions =======================================================================================
# Gets information about the 
# optimal period and relay from the webpage so it can be displayed on the webgraph and OLED screen
def get_all_info():
    try:
        response = requests.get(f"{webpageURL}/status")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error when retrieving status:", e)
        return None

def update_oled_display(optimal_start, optimal_end, is_currently_optimal, auto_mode_status, relay_status):

    image = Image.new('1', (oled.width, oled.height)) # The display first is set up with an empty image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    date = time.strftime("%H:%M   %d/%m/%y")

    # Setting up texts that will be displayed on the OLED, the text changes based on the information,
    new_display = {
        # text name : text then info variables e.g. Auto Mode: true
        "title_text": f"{date}",
        "optimal_period": "Optimal Period:",
        "optimal_period_2": f"{optimal_start} - {optimal_end}",
        "currently_optimal": "Currently Optimal: " + ("True" if is_currently_optimal else "False"),
        "auto_mode": "Auto Mode: " + ("On" if (auto_mode_status == "ON" or auto_mode_status is True) else "Off"),
        "relay_status": "Relay Status: " + ("On" if (relay_status == "ON" or relay_status is True) else "Off")
    }

    # the display is set blank, then the pixels of the text are set on
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    draw.text((0, 0), new_display["title_text"], font=font, fill=255) #new
    draw.text((0, 14), new_display["optimal_period"], font=font, fill=255) # Starts at 14 because pixels above are yellow for the OLED display
    draw.text((0, 24), new_display["optimal_period_2"], font=font, fill=255)
    draw.text((0, 34), new_display["currently_optimal"], font=font, fill=255)
    draw.text((0, 44), new_display["auto_mode"], font=font, fill=255)
    draw.text((0, 54), new_display["relay_status"], font=font, fill=255)

    oled.image(image)
    oled.show()
    # Now updates the display based on what changed from the previous display to reduce whole screen flashing
    previous_display.update(new_display)



# Makes the code loop based on an interval, as the display's response time is not significantly impacting the responsiveness of the system
while True:
    status = get_all_info()
    if status is not None: # This makes the display update only if the info is available
        optimal_period = status.get("optimalPeriod", "N/A")
        if optimal_period != "Data Unavailable" and " - " in optimal_period:
            optimal_start, optimal_end = optimal_period.split(" - ")
        else:
            optimal_start, optimal_end = "N/A", "N/A"

        # Changes the currently optimal field to bools to be used in update_oled_display()
        currently_optimal_str = status.get("currentlyOptimal", "False")
        is_currently_optimal = True if currently_optimal_str.lower() == "true" else False

        # Get auto mode and relay (Shelly switch) statuses.
        auto_mode_status = status.get("autoModeStatus", "OFF")
        relay_status = status.get("relayStatus", "OFF")

        # Update the OLED display with the latest information.
        update_oled_display(optimal_start, optimal_end, is_currently_optimal, auto_mode_status, relay_status)
    else:
        print("Could not retrieve information from the server") # For logging issues

    time.sleep(interval)
