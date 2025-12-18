#!/usr/bin/env python3
import subprocess
import json
import re
import requests
import time

# ---------- CONFIG ----------
NODE_ADDR = "[fd12:3456::92fd:9fff:feee:9d4b]"
COAP_PORT = 5683
THINGSPEAK_API_KEY = "API" # Replace with ThingSpeak API key
UPDATE_INTERVAL = 30  # seconds

# ---------- HELPERS ----------
def run_coap(cmd):
    """Run a CoAP command and return stdout as string."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")
        return ""

def time_to_minutes(timestr):
    """Convert Wi-SUN time format like '0-00:18:09' to total minutes."""
    m = re.match(r"(\d+)-(\d+):(\d+):(\d+)", timestr.strip())
    if not m:
        return 0.0
    days, hours, mins, secs = map(int, m.groups())
    total_mins = days * 24 * 60 + hours * 60 + mins + secs / 60.0
    return round(total_mins, 2)

def parse_neighbor_status(text):
    """Parse neighbor status text for rsl_in, rsl_out, and rpl_rank."""
    try:
        rsl_in = int(re.search(r'"rsl_in":\s*(-?\d+)', text).group(1))
        rsl_out = int(re.search(r'"rsl_out":\s*(-?\d+)', text).group(1))
        rpl_rank = int(re.search(r'"rpl_rank":\s*(\d+)', text).group(1))
        return rsl_in, rsl_out, rpl_rank
    except Exception as e:
        print(f"[ERROR] Failed to parse neighbor data: {e}")
        return 0, 0, 0

def extract_json_block(text):
    """Extract JSON object from text that may contain non-JSON lines."""
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        return None
    try:
        return json.loads(text[start:end])
    except Exception as e:
        print(f"[ERROR] JSON extraction failed: {e}")
        return None

# ---------- MAIN LOOP ----------
while True:
    try:
        print("\n==============================")
        print("📡 Collecting Wi-SUN node data...")
        print("==============================")

        # ---------- 1. Sensor data ----------
        sensor_cmd = f"aiocoap-client coap://{NODE_ADDR}:{COAP_PORT}/sensor/si7021"
        sensor_out = run_coap(sensor_cmd)
        sensor_json = extract_json_block(sensor_out)

        if sensor_json:
            temperature = sensor_json.get("temperature_mc", 0) / 1000.0
            humidity = sensor_json.get("humidity_mrh", 0) / 1000.0
        else:
            print("[ERROR] Could not parse sensor JSON.")
            temperature = humidity = 0.0

        # ---------- 2. Disconnected total ----------
        disc_cmd = f"aiocoap-client coap://{NODE_ADDR}:{COAP_PORT}/statistics/app/disconnected_total"
        disc_out = run_coap(disc_cmd)
        disconnected_total = time_to_minutes(disc_out.split("\n")[-1])

        # ---------- 3. Connected total ----------
        conn_cmd = f"aiocoap-client coap://{NODE_ADDR}:{COAP_PORT}/statistics/app/connected_total"
        conn_out = run_coap(conn_cmd)
        connected_total = time_to_minutes(conn_out.split("\n")[-1])

        # ---------- 4. Neighbor status ----------
        neighbor_cmd = f"aiocoap-client coap://{NODE_ADDR}:{COAP_PORT}/status/neighbor --payload 0"
        neighbor_out = run_coap(neighbor_cmd)
        rsl_in, rsl_out, rpl_rank = parse_neighbor_status(neighbor_out)

        # ---------- 5. Hopcount ----------
        status_cmd = f"aiocoap-client coap://{NODE_ADDR}:{COAP_PORT}/status/all"
        status_out = run_coap(status_cmd)
        status_json = extract_json_block(status_out)

        if status_json:
            hopcount = int(status_json.get("hopcount", 0))
        else:
            print("[ERROR] Could not parse hopcount JSON.")
            hopcount = 0

        # ---------- Print gathered data ----------
        print("\nCollected Data:")
        print(f"Temperature (°C): {temperature}")
        print(f"Humidity (%): {humidity}")
        print(f"Disconnected Total (min): {disconnected_total}")
        print(f"RSL In (dBm): {rsl_in}")
        print(f"RSL Out (dBm): {rsl_out}")
        print(f"RPL Rank: {rpl_rank}")
        print(f"Hopcount: {hopcount}")
        print(f"Connected Total (min): {connected_total}")

        # ---------- 6. Send to ThingSpeak ----------
        # Order: temperature, humidity, disconnected_total, rsl_in, rsl_out, rpl_rank, hopcount, connected_total
        url = "https://api.thingspeak.com/update"
        payload = {
            "api_key": THINGSPEAK_API_KEY,
            "field1": temperature,
            "field2": humidity,
            "field3": disconnected_total,
            "field4": rsl_in,
            "field5": rsl_out,
            "field6": rpl_rank,
            "field7": hopcount,
            "field8": connected_total,
        }

        resp = requests.post(url, data=payload, timeout=10)
        if resp.status_code == 200 and resp.text.strip() != "0":
            print(f"\n✅ Successfully sent to ThingSpeak (entry ID: {resp.text.strip()})")
        else:
            print(f"\n⚠ Failed to send to ThingSpeak: {resp.text} (status: {resp.status_code})")

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

    # ---------- Delay before next update ----------
    print(f"\n⏳ Waiting {UPDATE_INTERVAL} seconds before next update...\n")
    time.sleep(UPDATE_INTERVAL)
