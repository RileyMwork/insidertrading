from edgar.edgar_api_base import EdgarApiBase
from edgar.edgar_txt_file_parser import EdgarTxtFileParser

edgar_api = EdgarApiBase()
# links = edgar_api.get_recent_filings_txt_file_links_loop(start=0, end=1)

# edgar_txt_parser = EdgarTxtFileParser()

# parsed_data_list = []

# for link in links:
#     txt_file = edgar_txt_parser.get_txt_file(link)
#     parsed_data = edgar_txt_parser.parse_txt_file(txt_file)
#     parsed_data_list.append(parsed_data)

# print(parsed_data_list)


link = edgar_api.get_recent_filings_txt_file_links(filing_type="4", count=1, start=0)[0]
edgar_txt_parser = EdgarTxtFileParser()
txt_file = edgar_txt_parser.get_txt_file(link)
parsed_data = edgar_txt_parser.parse_txt_file(txt_file)
print(parsed_data)