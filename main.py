from edgar.controller.edgar_api_controller import EdgarApiController

edgar_api_controller = EdgarApiController()
info = edgar_api_controller.get_most_recent_transactions()
# print(info)