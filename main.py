# ---------------- EDGAR -----------------

from edgar.controller.edgar_api_controller import EdgarApiController
import pandas as pd

edgar_api_controller = EdgarApiController()
info = edgar_api_controller.get_most_recent_transactions()

# ---------------- EDGAR -----------------

# ---------------- ALPACA -----------------

# from alpaca_.api.account.alpaca_account_base import AlpacaAccountBase
# from alpaca_.api.assets.alpaca_assets_base import AlpacaAssetsBase
# from alpaca_.api.orders.alpaca_orders_base import AlpacaOrdersBase
# from alpaca_.api.positions.alpaca_positions_base import AlpacaPositionsBase

# account = AlpacaAccountBase()
# account_info = account.get_account()
# print(account_info.id)

# assets = AlpacaAssetsBase()
# assets_info = assets.get_assets()
# print(assets_info[0])
# print(len(assets_info))



# orders = AlpacaOrdersBase()


# order = orders.basic_order("AAPL", 1, "buy")
# print(order)

# limit_order = orders.limit_order("AAPL", 1, "buy", limit_price=200)
# print(limit_order)

# bracket_order = orders.bracket_order("AAPL", 1, "buy", take_profit_price=400, stop_loss_price=150)
# print(bracket_order)

# trailing_stop_order = orders.trailing_stop_order("AAPL", 1, "buy", trail_percent=1)
# print(trailing_stop_order)

# oco_order = orders.oco_order("AAPL", 1, limit_price=400, stop_loss_price=150, stop_limit_price=149.5)
# print(oco_order)

# positions = AlpacaPositionsBase()
# all_positions = positions.get_all_positions()
# print(all_positions)
# open_position = positions.get_position("LTCUSD")
# print(open_position)

# ---------------- ALPACA -----------------