from components.alpaca_.api.alpaca_api_base import AlpacaApiBase
from alpaca.trading.requests import LimitOrderRequest, LimitOrderRequest, MarketOrderRequest, StopLossRequest, TakeProfitRequest, TrailingStopOrderRequest
from alpaca.trading.enums import OrderClass, OrderSide, OrderType, TimeInForce
from components.alpaca_.repository.alpaca_insert import AlpacaInsert

class AlpacaOrdersBase(AlpacaApiBase):
    def __init__(self):
        super().__init__()
        self.alpaca_insert = AlpacaInsert()

    def basic_order(self, ticker, qty, side, time_in_force=TimeInForce.GTC, client_order_id=None):

        market_order_data = MarketOrderRequest(
                    symbol=ticker,
                    type=OrderType.MARKET,
                    qty=qty,
                    side=side,
                    time_in_force=time_in_force,
                    client_order_id=client_order_id
                    )

        market_order = self.trading_client.submit_order(order_data=market_order_data)

        return market_order
    
    def limit_order(self, ticker, qty, side, limit_price, time_in_force=TimeInForce.GTC, client_order_id=None):

        limit_order_data = LimitOrderRequest(
                    symbol=ticker,
                    type=OrderType.LIMIT,
                    limit_price=limit_price,
                    qty=qty,
                    side=side,
                    time_in_force=time_in_force,
                    client_order_id=client_order_id
                    )

        limit_order = self.trading_client.submit_order(order_data=limit_order_data)
        
        return limit_order
    
    def bracket_order(self, ticker, qty, side, take_profit_price, stop_loss_price, time_in_force=TimeInForce.GTC, client_order_id=None):

        bracket__order_data = MarketOrderRequest(
                    symbol=ticker,
                    qty=qty,
                    type=OrderType.MARKET,
                    side=side,
                    time_in_force=time_in_force,
                    order_class=OrderClass.BRACKET,
                    take_profit=TakeProfitRequest(limit_price=take_profit_price),
                    stop_loss=StopLossRequest(stop_price=stop_loss_price),
                    client_order_id=client_order_id
                    )

        bracket_order = self.trading_client.submit_order(
                order_data=bracket__order_data
            )
        
        self.alpaca_insert.insert_new_order_info([ticker, bracket_order.created_at, bracket_order.expires_at, "bracket", 
                                                bracket_order.side, bracket_order.time_in_force, qty, bracket_order.filled_qty, 
                                                bracket_order.filled_avg_price, take_profit_price, stop_loss_price, None])
        
        return bracket_order
    
    def trailing_stop_order(self, ticker, qty, side, trail_percent, time_in_force=TimeInForce.GTC, client_order_id=None):

        trailing_order_data = TrailingStopOrderRequest(
                    symbol=ticker,
                    type=OrderType.LIMIT,
                    qty=qty,
                    side=side,
                    time_in_force=time_in_force,
                    trail_percent=trail_percent,
                    client_order_id=client_order_id
                    )

        trailing_percent_order = self.trading_client.submit_order(
                order_data=trailing_order_data
            )
        
        return trailing_percent_order
    
    def oco_order(self, ticker, qty, limit_price, stop_loss_price, stop_limit_price, time_in_force=TimeInForce.GTC, client_order_id=None):

        oco_order_data = LimitOrderRequest(
                symbol=ticker,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=time_in_force,
                order_class=OrderClass.OCO,
                take_profit={
                    "limit_price": limit_price
                },
                stop_loss={
                    "stop_price": stop_loss_price,
                    "limit_price": stop_limit_price
                },
                client_order_id=client_order_id
            )       

        oco_order = self.trading_client.submit_order(
                order_data=oco_order_data
            )
        
        return oco_order