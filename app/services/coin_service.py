from fastapi import HTTPException
from schemas.coin import CoinInfo
from utils.constants import COIN_MAPPING, COINMARKETCAP_API_KEY
from coinmarketcapapi import CoinMarketCapAPI


def get_coin_data_from_broker_api(coin_name: str):
    coin_position = COIN_MAPPING[coin_name]

    cmc_api = CoinMarketCapAPI(COINMARKETCAP_API_KEY)
    coin_data = cmc_api.cryptocurrency_listings_latest(limit=10).data[coin_position]
    usd_data = coin_data["quote"]["USD"]

    coin_info = CoinInfo(
        name=coin_data["name"],
        price=usd_data["price"],
        volume_24h=usd_data["volume_24h"],
        percent_change_1h=usd_data["percent_change_1h"],
        percent_change_24h=usd_data["percent_change_24h"],
        percent_change_7d=usd_data["percent_change_7d"],
    )
    return coin_info
