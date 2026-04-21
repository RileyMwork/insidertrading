from controllers.edgar_controllers.edgar_api_controller import EdgarApiController
from infrastructure.enums.db_file_paths import DbFilePath
from repository.db_connect import DbConnect

# edgar_api_controller = EdgarApiController()
# info = edgar_api_controller.get_edgar_df()
# print(info)

db_connect = DbConnect(DbFilePath.EDGAR_DB_FILE_PATH.value)

db_connect.select()