import requests
import os
import json
import pandas as pd
import time
from dotenv import load_dotenv
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from tradingview_websocket import TradingViewWebSocket

load_dotenv()

API_URL = os.getenv("API_URL")
HEADERS = json.loads(os.getenv("HEADERS"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
SUPABASE_API_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")


def collect_tv():
    url = f"{SUPABASE_URL}/rest/v1/symbol_timeframes?select=*,symbols(*,exchanges(*)),timeframes(*)"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    rows = []
    for item in data:
        symbol_info = item.get("symbols", {})
        exchange_info = symbol_info.get("exchanges", {})
        timeframe_info = item.get("timeframes", {})

        rows.append({
            "symbol_timeframe_id": item["id"],
            "symbol": symbol_info.get("symbol"),
            "exchange_name": exchange_info.get("name"),
            "timeframe": timeframe_info.get("name")
        })

    df = pd.DataFrame(rows)

    results = []

    for _, row in df.iterrows():
        id_timeframe = row["symbol_timeframe_id"]
        exchange_name = row["exchange_name"]
        symbol = row["symbol"]
        timeframe = row["timeframe"]

        try:
            url = f"{API_URL}/{id_timeframe}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Kiểm tra dữ liệu trống hay không
                if isinstance(data, list) and len(data) == 0:
                    candles = 20000
                else:
                    candles = 5

                results.append({
                    "symbol_timeframe_id": id_timeframe,
                    "exchange_name": exchange_name,
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "candles": candles
                })
            else:
                print(f"Lỗi {response.status_code} khi truy cập {url}")

        except Exception as e:
            print(f"Lỗi khi gọi API {id_timeframe}: {e}")

    # Tạo DataFrame kết quả
    result_df = pd.DataFrame(results)

    def post_to_api(data, max_retries=3, retry_delay=5):
        for i in range(0, len(data), BATCH_SIZE):
            batch = data[i:i + BATCH_SIZE] 
            batch_num = i // BATCH_SIZE + 1
            
            for attempt in range(1, max_retries + 1):
                try:
                    response = requests.post(f"{API_URL}/", headers=HEADERS, json=batch, timeout=60)

                    if response.status_code in [200, 201]:
                        print(f"🚀 Uploaded batch {batch_num} ({len(batch)} rows)")
                        break  # success → thoát retry loop
                    
                    else:
                        print(f"⚠️ Batch {batch_num} failed (attempt {attempt}/{max_retries}): "
                            f"{response.status_code} - {response.text}")

                except Exception as e:
                    print(f"❌ Error uploading batch {batch_num} (attempt {attempt}/{max_retries}): {e}")

                # Nếu chưa hết lượt retry thì chờ trước khi thử lại
                if attempt < max_retries:
                    time.sleep(retry_delay)
            else:
                # Nếu sau max_retries vẫn lỗi
                print(f"🚫 Batch {batch_num} permanently failed after {max_retries} attempts.")


    for _, row in result_df.iterrows(): 
        tradingview_symbol = f"{row['exchange_name']}:{row['symbol']}"
        timeframe = row["timeframe"]
        candles = row["candles"]
        symbol_timeframe_id = row["symbol_timeframe_id"]

        print(f"▶ Fetching {tradingview_symbol} | {timeframe} | {candles} candles")

        # --- lấy dữ liệu từ TradingView ---
        ws = TradingViewWebSocket(tradingview_symbol, timeframe, candles)
        ws.connect()
        ws.run()
        result_data = ws.result_data

        all_candles = []
        for item in result_data:
            v = item["v"]
            all_candles.append({
                "symbol_timeframe_id": symbol_timeframe_id,
                "open": v[1],
                "high": v[2],
                "low": v[3],
                "close": v[4],
                "volume": v[5],
                "recorded_at": datetime.fromtimestamp(v[0], tz=timezone.utc)
                    .astimezone(ZoneInfo("America/New_York"))
                    .strftime("%Y-%m-%dT%H:%M:%SZ")
            })

        # --- GỬI LÊN API ---
        post_to_api(all_candles)

    print(f"✅ Hoàn thành thu thập dữ liệu vào lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")