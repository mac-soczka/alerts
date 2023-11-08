import json
from datetime import datetime, timedelta
import time
import httpx
import asyncio
from Alert import Alert

# api keys - to be moved outside of git
read_api_key = "ba29f4f9-9c6e-4023-98cd-fb576b3b7b3c"

# authentication to be added at a later stage
save_api_key = ""

coinbase_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
backend_url = 'http://localhost:5000/'
bot_url = "https://f9bb-82-43-212-31.ngrok-free.app"

coinbase_params = {
    'convert': 'USD',
    'symbol': 'BTC,ETH,TON'
}

headers = {
    'Accepts': 'application/json',
}

cryptocurrencies = ['BTC', 'ETH', "TON"]

INTERVAL = 60  # in seconds


async def read_data(url, params=None, headers=None):
    if (url == coinbase_url):
        headers['X-CMC_PRO_API_KEY'] = read_api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            raw_data = response.json()
            return raw_data
    
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


async def save_data(data):
    async with httpx.AsyncClient() as client:
        headers['X-CMC_PRO_API_KEY'] = save_api_key
        tasks = []
        prices = {}
        prices_url = backend_url + "prices"
        for crypto in cryptocurrencies:
            price_val = unpack(data, crypto)

            payload = {
                'cryptocurrency': crypto,
                'value': price_val
            }
            prices[crypto] = price_val
            tasks.append(client.post(
                prices_url, json=payload, headers=headers))

        try:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for crypto, response in zip(cryptocurrencies, responses):
                if isinstance(response, httpx.Response):
                    print(
                        f"{timestamp} - Status Code for {crypto}: {response.status_code}")
                else:
                    print(f"{timestamp} - Error with {crypto}: {response}")

            return prices

        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"{timestamp} - An unexpected error occurred while saving data: {e}")


def unpack(packed, coin):
    coindata = packed['data'][coin]
    return coindata['quote']['USD']['price']


async def should_fire_alerts(current_prices):
    print("Checking alerts...")
    now = datetime.now()
    alerts_url = backend_url + "alerts" 
    alerts = await read_data(alerts_url, headers=headers)
    alert_objs = [Alert(**data) for data in alerts]

    for alert in alert_objs:
        if alert.expires_at < now:
            return

        crypto = alert.cryptocurrency
        if crypto in current_prices:
            current_price = current_prices[crypto]
            price_change = current_price - alert.base_value

            if alert.trigger_type == 'percent_change':
                percent_change = (price_change / alert.base_value) * 100
                if abs(percent_change) >= alert.trigger_value:
                  await handle_alert_due(alert, current_price, percent_change)
            elif alert.trigger_type == 'value_change':
                if abs(price_change) >= alert.trigger_value:
                  await handle_alert_due(alert, current_price, price_change)


async def handle_alert_due(alert, current_price, change_value):
    print(f"Alert {alert.id} type {alert.trigger_type} with value {alert.trigger_value} is due for cryptocurrency {alert.cryptocurrency} for user {alert.user_id}.")
    print(f"Current Price: {current_price:.2f}, Change: {change_value:.2f}")

    message = f"Alert {alert.id} for cryptocurrency {alert.cryptocurrency} of type {alert.trigger_type} has changed by {change_value:.2f} from {alert.base_value} and is due."
    user_id = alert.user_id
    if user_id == "mac":
        return

    content = {
       "message" : message,
       "user_id" : user_id
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(bot_url+"/trigger", json=content)
            response.raise_for_status()
            raw_data = response.json()
            print(raw_data)
            return raw_data
    
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # TODO
    # call bot webhoo
    # mark alert as fired
    


async def main():
    while True:
        try:
            raw_data = await read_data(coinbase_url, coinbase_params, headers=headers)
            if raw_data:
                prices = await save_data(raw_data)
                if prices:
                    await should_fire_alerts(prices)
        except Exception as e:
            print(f"An unexpected error occurred in main loop: {e}")
        finally:
            await asyncio.sleep(INTERVAL)
if __name__ == "__main__":
    asyncio.run(main())
