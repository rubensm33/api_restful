from sqlalchemy.orm import Session

from models.coin import Coin


def save_coin(db: Session, coin_data: Coin, user_id: int):

    coin = Coin(
        name=coin_data.name,
        user_id=user_id,
        price=coin_data.price,
        quantity=coin_data.quantity,
        volume_24h=coin_data.volume_24h,
        percent_change_1h=coin_data.percent_change_1h,
        percent_change_24h=coin_data.percent_change_24h,
        percent_change_7d=coin_data.percent_change_7d,
    )
    db.add(coin)
    db.commit()
    db.refresh(coin)
    return coin
