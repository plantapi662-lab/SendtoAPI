import requests
import time
import sys

SOURCE_STOCK = "https://api.giahuy.dpdns.org/api/pvb/stock"
TARGET_STOCK = "https://plantsourcecodeapi.onrender.com/api/pvbr/stock"

SOURCE_WEATHER = "https://api.giahuy.dpdns.org/api/weather"
TARGET_WEATHER = "https://plantsourcecodeapi.onrender.com/api/pvbr/weather"

def sync_api(source_url, target_url, name):
    try:
        response = requests.get(source_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        post_response = requests.post(target_url, json=data, timeout=10)
        post_response.raise_for_status()

        print(f"[OK] {name} synced", flush=True)

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {name} -> {e}", flush=True)

while True:
    print("⏱️ Sync cycle...", flush=True)

    sync_api(SOURCE_STOCK, TARGET_STOCK, "STOCK")
    sync_api(SOURCE_WEATHER, TARGET_WEATHER, "WEATHER")

    time.sleep(5)
