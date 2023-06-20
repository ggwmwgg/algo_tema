import asyncio
import os
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from utils.func import notifier, get_df
import datetime
import threading
from dotenv import load_dotenv


def state_checker(old_state, new_state, open_price, close_price, time, curr_time, indc_name):
    """
    Gets old and new state of indicator, open and close price, bar time, current time and indicator name
    \nIf old and new state are different, prints message and notifier() function is called
    """
    if old_state != new_state:
        if new_state != "none":
            text = f"{curr_time}:{indc_name} | {open_price:.2f} | {close_price:.2f} | state: {new_state} | bar_time: {time} | was: {old_state} | time: {curr_time}"
            notifier(text)

            return new_state
        else:
            return old_state
    else:
        return old_state


def checker(api_key, api_secret, len_m, coin_symbol, client):
    last_time = None
    state = "none"
    updated = False

    def process_message(message):
        nonlocal state
        nonlocal last_time
        nonlocal updated
        # Process the received message
        non_historical = client.get_klines(symbol=coin_symbol, interval=Client.KLINE_INTERVAL_15MINUTE,
                                           limit=len_m * len_m * len_m)
        # print(non_historical)
        df = get_df(non_historical)

        tema_open = df["tema_open"]
        tema_close = df["tema_close"]

        exp = lambda a, b: "long" if a > b else "short" if a < b else "none"

        min_s = (non_historical[-1][0] + 60000) / 1000
        max_s = (non_historical[-1][0] + 70000) / 1000

        if last_time != non_historical[-1][0] or last_time is None:
            updated = False
            if last_time is None:
                curr_time = datetime.datetime.utcnow().strftime("%d.%m.%y %H:%M:%S")
                if state != exp(tema_open[-1], tema_close[-1]):
                    updated = True
                    state = state_checker(state, exp(tema_open[-1], tema_close[-1]), tema_open[-1], tema_close[-1],
                                           df.index[-1], curr_time, "TEMA1.0")
                last_time = non_historical[-1][0]

        if max_s > datetime.datetime.now().timestamp() > min_s and not updated:
            if state != exp(tema_open[-1], tema_close[-1]):
                curr_time = datetime.datetime.utcnow().strftime("%d.%m.%y %H:%M:%S")
                if state != exp(tema_open[-1], tema_close[-1]):
                    updated = True
                    state = state_checker(state, exp(tema_open[-1], tema_close[-1]), tema_open[-1], tema_close[-1],
                                          df.index[-1], curr_time, "TEMA1.0")

    # Create a websocket manager instance
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)

    # Start the websocket manager
    twm.start()

    # Subscribe to the BTC/USDT 1-minute candlestick stream
    coin_interval = '1m'
    # Futures
    # twm.start_kline_futures_socket(callback=process_message, symbol=coin_symbol, interval=coin_interval)
    # twm.start_kline_futures_socket(callback=process_message, symbol=coin_symbol, interval=coin_30m_interval)
    # Spot
    twm.start_kline_socket(callback=process_message, symbol=coin_symbol, interval=coin_interval)

    twm.join()


def run_checker(api_key, api_secret, len, coin_symbol, client):
    # Create an event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Run the checker function within the event loop
    loop.run_until_complete(checker(api_key, api_secret, len, coin_symbol, client))


def main():
    # Create the first thread with sym1 argument
    load_dotenv()
    api_key_main = os.getenv("binance_key")
    api_secret_main = os.getenv("binance_secret")
    len_main = 8
    client_main = Client(api_key_main, api_secret_main)
    symbol_list = ["BTCUSDT"]
    threads = []

    for symbol in symbol_list:
        thread = threading.Thread(target=run_checker,
                                  args=(api_key_main, api_secret_main, len_main, symbol, client_main))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    print("Starting...")
    main()
