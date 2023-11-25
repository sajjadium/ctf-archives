import time
import random

def get_coin_price_from_api(coin: str):
    coins = coin.split('/')
    if(len(coins) != 2):
        return []
    seed = coins[0] + coins[1] if coins[0] < coins[1] else coins[1] + coins[0]
    is_reverse = coins[0] < coins[1]
    random.seed(seed)
    end_timestamp = int(time.time()) * 1000

    new_open = 15.67
    new_high = 15.83
    new_low = 15.24
    new_close = 15.36

    new_volume = 3503100
    movement = 0.7

    data = []
    max_ticks = 200
    for ts in range(0, max_ticks):

        display_new_open = 1. / new_open if is_reverse else new_open
        display_new_high = 1. / new_high if is_reverse else new_high
        display_new_low = 1. / new_low if is_reverse else new_low
        display_new_close = 1. / new_close if is_reverse else new_close

        data.append({
            "Date": end_timestamp - (max_ticks - ts) * (1000 * 86400), 
            "Open":  display_new_open, 
            "High":  display_new_high, 
            "Low":  display_new_low, 
            "Close": display_new_close, 
            "Volume": new_volume 
        })

        # New Open => Downwards Trend
        # New Close => Upwards Trend
        indicator = new_open if random.random() > 0.5 else new_close

        new_open = indicator + movement * (random.random() - 0.5)
        new_high = indicator + movement * (random.random() - 0.5)
        new_low = indicator + movement * (random.random() - 0.5)
        new_close = indicator + movement * (random.random() - 0.5)
        new_volume = new_volume + movement * (random.random() - 0.5)
    return data
