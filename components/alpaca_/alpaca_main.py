from alpaca_.service.alpaca_service import AlpacaService

alpaca_service = AlpacaService()

intervals = alpaca_service.generate_intervals("2024-01-16")
print(intervals)