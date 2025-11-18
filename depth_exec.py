def simulate_fill(orderbook_side, amount, is_buy=True):
    """
    orderbook_side — список уровней: [[price, qty], ...]
    amount — сколько base-asset хотим купить/продать
    is_buy=True — для ордера BUY мы потребляем ASK-сторону

    Возвращает:
        (avg_price, executed_amount) или (None, 0) если не хватило глубины
    """

    remaining = amount
    cost = 0.0

    for level_price, level_qty in orderbook_side:
        level_price = float(level_price)
        level_qty = float(level_qty)

        if remaining <= 0:
            break

        consumed = min(remaining, level_qty)
        cost += consumed * level_price
        remaining -= consumed

    if remaining > 0:
        # Глубины не хватило — сделка не исполнима на нужном объёме
        return None, 0

    avg_price = cost / amount
    return avg_price, amount
