import requests
import time
from datetime import datetime

SOURCE_STOCK = "https://api.giahuy.dpdns.org/api/pvb/stock"
TARGET_STOCK = "https://plantsourcecodeapi.onrender.com/api/pvbr/stock"

SOURCE_WEATHER = "https://api.giahuy.dpdns.org/api/weather"
TARGET_WEATHER = "https://plantsourcecodeapi.onrender.com/api/pvbr/weather"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; RenderBot/1.0)",
    "Accept": "application/json",
    "Connection": "keep-alive"
}

NORMAL_DELAY = 30      # secondes entre chaque cycle normal
ERROR_DELAY = 120      # pause après erreur
FORBIDDEN_DELAY = 300  # pause après 403 (5 min)

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def sync_api(source_url, target_url, name):
    try:
        response = requests.get(
            source_url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 403:
            log(f"[403] {name} access forbidden — sleeping {FORBIDDEN_DELAY}s")
            time.sleep(FORBIDDEN_DELAY)
            return False

        response.raise_for_status()
        data = response.json()

        post_response = requests.post(
            target_url,
            json=data,
            timeout=10
        )
        post_response.raise_for_status()

        log(f"[OK] {name} synced")
        return True

    except requests.exceptions.RequestException as e:
        log(f"[ERROR] {name} -> {e}")
        time.sleep(ERROR_DELAY)
        return False

def main():
    log("🚀 API Sync started")

    while True:
        success_stock = sync_api(SOURCE_STOCK, TARGET_STOCK, "STOCK")
        success_weather = sync_api(SOURCE_WEATHER, TARGET_WEATHER, "WEATHER")

        if success_stock and success_weather:
            log(f"⏱️ Cycle done — sleeping {NORMAL_DELAY}s")
            time.sleep(NORMAL_DELAY)
        else:
            log(f"⚠️ Error detected — retry later")

if __name__ == "__main__":
    main()
