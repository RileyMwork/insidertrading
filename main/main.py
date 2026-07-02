from main.components.edgar.controller.edgar_controller import EdgarController

edgar_controller = EdgarController()

edgar_controller.get_transactions(start_date="2023-02-07", end_date="2023-02-08")


