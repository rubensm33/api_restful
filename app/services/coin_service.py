from models.coin import Coin

def get_coin_data_from_broker_api():
    """
    Mock Data.
    """
    data = {
        "name": "Bitcoin",
        "price": 5.65,
        "volume_24h": 7155680000,
        "quantity": 2,
        "percent_change_1h": -0.152774,
        "percent_change_24h": 0.518894,
        "percent_change_7d": 0.986573,
    }
    return Coin(**data)
