import requests
import plotly.graph_objects as go
from plotly.io import to_json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta, date, timezone
import time
from threading import Thread
import tzlocal

app = Flask(__name__, template_folder=".")

# get the local timezone
local_tz = tzlocal.get_localzone()

# Variables to be changed =========================================================================================================================================================

# Shelly relay variables
SERVER_URI = "Put your shelly's uri here, it'll likely look like: shelly-x-eu.shelly.cloud"
DEVICE_ID = "Put your shelly relay's id here"
AUTH_KEY = "Place your auth key for your account here"

# Agile Octopus API variables
region_code = "B" # this is the region code for east midlands (e.g. Lincolnshire), see the readme for a table of the UK's region codes
product_code = "AGILE-24-10-01" # Agile Octopus tariff code, 
electricity_tariff_type = "E-1R"
period_size = 1  # how long the appliance should be switched on for per day, each period is 30 minutes (2 periods would therefore be 1 hour of on-time, 23 hrs off-time)

INTERVAL = 2  # determines how quickly the script loops, this variable can be increased to decrease load on your Raspberry Pi if it's having trouble.

# End of variables to be changed  ================================================================================================================================================

automatic_mode = True
start_time_global = None
end_time_global = None


# Optimal Period calc ===============================================================
def retrieve_energy_data_from_api(target_date):
    tomorrow = target_date + timedelta(days=1)
    day_start = datetime.combine(target_date, datetime.min.time(), tzinfo=local_tz).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    day_end = datetime.combine(tomorrow, datetime.min.time(), tzinfo=local_tz).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    tariff_code = f"{electricity_tariff_type}-{product_code}-{region_code}"
    base_url = f"https://api.octopus.energy/v1/products/{product_code}/electricity-tariffs/{tariff_code}/standard-unit-rates/"
    params = {"period_from": day_start, "period_to": day_end}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            df = pd.DataFrame(results)
            df["Time Period"] = pd.to_datetime(df["valid_from"]).dt.tz_convert(timezone.utc) # fixed
            df["Price"] = df["value_inc_vat"]
            return df[["Time Period", "Price"]]
        else:
            print(f"Could not find data for {target_date}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Could not retrieve data from Octopus Energy API: {e}")
        return None

# cycle through the periods to find lowest price
def find_optimal_period(df):
    min_average_price = float("inf")
    optimal_start_index = 0
    
    if df is None or len(df) < period_size:
        return None, None
    for i in range(len(df) - period_size + 1):
        period_average = df["Price"].iloc[i : i + period_size].mean()
        if period_average < min_average_price:
            min_average_price = period_average
            optimal_start_index = i
    return (
        df.iloc[optimal_start_index : optimal_start_index + period_size],
        min_average_price,
    )

# Save the optimal period start and end times, and define what the relay should do during and outside optimal period
def update_optimal_period():
    global start_time_global, end_time_global
    today = date.today()
    df = retrieve_energy_data_from_api(today)

    if df is not None:
        optimal_period_df, average_price = find_optimal_period(
            df.sort_values(by= "Time Period").reset_index(drop=True)
        )
        if optimal_period_df is not None and not optimal_period_df.empty:
            start_time = optimal_period_df["Time Period"].iloc[0]
            end_time = optimal_period_df["Time Period"].iloc[-1] + timedelta(minutes = 30)

            start_time_global = start_time
            end_time_global = end_time

            current_time_utc = datetime.now(timezone.utc)

            if start_time <= current_time_utc < end_time:
                state = switch_relay("on")
                print(f"Relay switched ON for optimal period. Status: {state}")
            else:
                state = switch_relay("off")
                print(f"Relay switched OFF as currently outside optimal period. Status: {state}")
        else:
            print("Could not find optimal period for today")
            switch_relay("off")
            start_time_global = None
            end_time_global = None
    else:
        print("Could not retrieve the energy data for today.")
# ===================================================================================================================================================


# Relay Control =====================================================================================================================================
def relay_status():
    url = f"https://{SERVER_URI}/device/status"
    data = {"id": DEVICE_ID, "auth_key": AUTH_KEY}
    try:
        response = requests.post(url, data = data)
        response.raise_for_status()
        device_data = response.json().get("data", {})
        device_status = device_data.get("device_status", {})
        relay_info = device_status.get("switch:0", {})
        return relay_info.get("output", False)
    except requests.exceptions.RequestException as e:
        print(f"Error checking relay status: {e}")
        return False

# communicate with the shelly relay over cloud
def switch_relay(turn_state):
    url = f"https://{SERVER_URI}/device/relay/control"
    data = {"channel": 0, "turn": turn_state, "id": DEVICE_ID, "auth_key": AUTH_KEY}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when trying to control the relay: {e}")
        return {"error": str(e)}


# code to host the webpage locally, which will allow controlling the iot system from PCs, phones etc. on the local network ==================
@app.route("/")
# make a graph for the webpage to visually show the energy prices
def display_graph():
    global start_time_global, end_time_global
    today = date.today()
    df = retrieve_energy_data_from_api(today)

    graph_json = "{}"
    error_message = None

    if df is not None:
        df_sorted = df.sort_values(by="Time Period").reset_index(drop=True)
        optimal_period_df, average_price = find_optimal_period(df_sorted.copy())

        start_time_utc = None
        end_time_utc = None

        if optimal_period_df is not None and not optimal_period_df.empty:
            start_time_utc = optimal_period_df["Time Period"].iloc[0]
            end_time_utc = optimal_period_df["Time Period"].iloc[-1] + timedelta(minutes=30)
            start_time_global = start_time_utc
            end_time_global = end_time_utc
        else:
             if start_time_global and start_time_global.date() == start_time_utc.astimezone(local_tz).date():
                 start_time_global = None
                 end_time_global = None
             average_price = None


        fig = go.Figure()

        df_sorted["Time Period Local"] = df_sorted["Time Period"].dt.tz_convert(local_tz)

        fig.add_trace(
            go.Bar(
                x=df_sorted["Time Period Local"].dt.strftime("%H:%M"),
                y=df_sorted["Price"],
                hovertemplate="Time: %{x}<br>Price: %{y:.2f} p/kWh",
                marker=dict(color=df_sorted["Price"], coloraxis="coloraxis"),
                name="",
            )
        )

        if start_time_utc and end_time_utc and average_price is not None:
            start_time_local_display = start_time_utc.astimezone(local_tz)
            end_time_local_display = end_time_utc.astimezone(local_tz)

            period_duration_minutes = period_size * 30
            if period_duration_minutes >= 60 and period_duration_minutes % 60 == 0:
                duration_text = f"{period_duration_minutes // 60}-Hour"
            else:
                duration_text = f"{period_duration_minutes}-Minute"


            fig.add_annotation(
                x = start_time_local_display.strftime("%H:%M"),
                y = df_sorted["Price"].max() * 1.1 if not df_sorted.empty else 1,
                text = (
                    f"Optimal {duration_text} period: {start_time_local_display.strftime('%H:%M')} - {end_time_local_display.strftime('%H:%M')}<br>"
                    f"Average Price: {average_price:.2f} p/kWh" # 2 decimal places
                ),
                showarrow = False,
                bgcolor = "yellow",
                font = dict(size=16),
            )
        # bug fix 2
        try:
            tz_name = local_tz.key
        except AttributeError:
            tz_name = str(local_tz)

        fig.update_layout(
            xaxis_title=f"Time Period ({tz_name})",
            yaxis_title="Price (p/kWh)",
            coloraxis = dict(colorbar=dict(title="Price (p/kWh)")),
            autosize = True,
        )

        graph_json = to_json(fig)
    else:
        error_message="Could not retrieve energy data."

    # use the webpage
    return render_template(
        "webpage.html",
        graph_json = graph_json,
        interval = INTERVAL,
        automaticMode = automatic_mode,
        error = error_message
    )



@app.route("/status")
# Set what the relay status should be
# 2c 
def get_relay_status():
    global start_time_global, end_time_global
    current_status = relay_status()
    display_relay_status = "ON" if current_status else "OFF"
    auto_mode_status = "ON" if automatic_mode else "OFF"

    current_time_utc = datetime.now(timezone.utc)

    optimal_period_display = "Calculating Optimal Period"
    currently_optimal = "False"

    if start_time_global and end_time_global:
        if start_time_global.astimezone(local_tz).date() == current_time_utc.astimezone(local_tz).date():
            start_time_local_display = start_time_global.astimezone(local_tz)
            end_time_local_display = end_time_global.astimezone(local_tz)
            try:
                tz_name = local_tz.key
            except AttributeError:
                tz_name = str(local_tz)
            optimal_period_display = f"{start_time_local_display.strftime('%H:%M')} - {end_time_local_display.strftime('%H:%M')} ({tz_name})"

            if start_time_global <= current_time_utc < end_time_global:
                 currently_optimal = "True"
            else:
                 currently_optimal = "False"
        else:
             optimal_period_display = "Waiting for today's data"
             currently_optimal = "False"
    else:
        optimal_period_display = "Optimal period data is unavailable"
        currently_optimal = "False"

    return jsonify(
        optimalPeriod=optimal_period_display,
        currentlyOptimal=currently_optimal,
        autoModeStatus=auto_mode_status,
        relayStatus=display_relay_status,
    )

# Webpage buttons ================================
@app.route("/switch_relay", methods=["POST"])
def switch_relay_route():
    turn_state = request.form["turnState"]
    switch_relay(turn_state)
    return redirect(url_for("display_graph"))


@app.route("/toggle_auto_mode", methods=["POST"])
def toggle_auto_mode():
    global automatic_mode
    automatic_mode = not automatic_mode
    return redirect(url_for("display_graph"))


def run_automatic_mode():
    while True:
        if automatic_mode:
            update_optimal_period()
        time.sleep(INTERVAL)
# ===================================================

automatic_thread = Thread(target = run_automatic_mode)
automatic_thread.daemon = True
automatic_thread.start()

if __name__ == "__main__":
    try:
        tz_name = local_tz.key
    except AttributeError:
        tz_name = str(local_tz)
    print(f"Found local timezone: {tz_name}")
    print("Starting Webpage")
    app.run(host = "0.0.0.0", port=8080, debug=False) # run it locally
