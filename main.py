from edgar.edgar_api_base import EdgarApiBase
from edgar.edgar_txt_fetcher import EdgarTxtFetcher

edgar_api = EdgarApiBase()
txt_links = edgar_api.get_recent_filings_txt_links()

edgar_txt_fetcher = EdgarTxtFetcher()
txt_files = edgar_txt_fetcher.fetch_all(txt_links[0:3], max_workers=5)

























































































# from edgar.edgar_api_base import EdgarApiBase
# from edgar.edgar_xml_file_parser import EdgarXMLFileParser
# from edgar.edgar_index_html_parser import EdgarIndexHtmlParser
# import pandas as pd


# edgar_api = EdgarApiBase()
# index_links = edgar_api.get_recent_filings_txt_file_links_loop(filing_type="4", count=10, start=0, end=10)
# index_html_list = []
# for index_link in index_links:
#     index_html = edgar_api.get_index_html(index_link)
#     index_html_list.append(index_html)

# edgar_index_html_parser = EdgarIndexHtmlParser()
# xml_links_list = []
# for i in index_html_list:
#     xml_links = edgar_index_html_parser.parse_index_html(i)
#     xml_links_list.append(xml_links)    



# edgar_index_xml_parser = EdgarXMLFileParser()
# xml_files = []
# for xml_link in xml_links_list:
#     xml_file = edgar_api.get_xml_file(xml_link)
#     xml_files.append(xml_file)

# entries = []
# for xml_file in xml_files:
#     issuer_info = edgar_index_xml_parser.get_issuer_info(xml_file)
#     reporting_owner_ids = edgar_index_xml_parser.get_reporting_owner_ids(xml_file)
#     reporting_owner_address = edgar_index_xml_parser.get_reporting_owner_address(xml_file)
#     reporting_owner_relationship = edgar_index_xml_parser.get_reporting_owner_relationship(xml_file)
#     non_derivative_transactions = edgar_index_xml_parser.get_non_derivative_transactions(xml_file)

# print(non_derivative_transactions)

    # for i in non_derivative_transactions:
    #     entry = {i[0]: i[1]}
    #     for j in issuer_info:
    #         entry[j[0]] = j[1]
    #     for j in reporting_owner_ids:
    #         entry[j[0]] = j[1]
    #     for j in reporting_owner_address:
    #         entry[j[0]] = j[1]
    #     for j in reporting_owner_relationship:
    #         entry[j[0]] = j[1]
    #     entries.append(entry)


# df = pd.DataFrame(entries)
# print(df)
# df.to_csv("insider_trading_data.csv", index=False)

# a = edgar_index_xml_parser.get_issuer_info(xml_file)
# b = edgar_index_xml_parser.get_reporting_owner_ids(xml_file)
# c = edgar_index_xml_parser.get_reporting_owner_address(xml_file)
# d = edgar_index_xml_parser.get_reporting_owner_relationship(xml_file)
# e = edgar_index_xml_parser.get_non_derivative_transactions(xml_file)

# print(e)

# entry = {}
# for i in a:
#     entry[i[0]] = i[1]
# for i in e:
#     entry[i[0]] = i[1]
# print(entry)


# for i in issuer_info_values:
#     entry[i[0]] = i[1]
# for i in reporting_owner_info_values:
#     entry[i[0]] = i[1]
# for i in reporting_owner_address_values:
#     entry[i[0]] = i[1]
# for i in reporting_owner_relationship_values:
#     entry[i[0]] = i[1]
# print(entry)

# doc = BeautifulSoup(xml_file, "xml")

# entry = {}

# issuer_info = doc.find("issuer")
# issuer_info_values = []
# for i in issuer_info.find_all():
#     name = i.name
#     text = i.text.strip()
#     issuer_info_values.append((name, text))



# reporting_owner_info = doc.find("reportingOwner")
# reporting_owner_id = reporting_owner_info.find("reportingOwnerId")
# reporting_owner_info_values = []
# for i in reporting_owner_id.find_all():
#     name = i.name
#     text = i.text.strip()
#     reporting_owner_info_values.append((name, text))
# reporting_owner_address = reporting_owner_info.find("reportingOwnerAddress")
# reporting_owner_address_values = []
# for i in reporting_owner_address.find_all():
#     name = i.name
#     text = i.text.strip()
#     reporting_owner_address_values.append((name, text))
# reporting_owner_relationship = reporting_owner_info.find("reportingOwnerRelationship")
# reporting_owner_relationship_values = []
# for i in reporting_owner_relationship.find_all():
#     name = i.name
#     text = i.text.strip()
#     reporting_owner_relationship_values.append((name, text))



# non_derivative_table = doc.find("nonDerivativeTable")
# non_derivative_transactions = non_derivative_table.find_all("nonDerivativeTransaction")
# for i in non_derivative_transactions:
#     security_title = i.find("securityTitle")
#     for j in security_title.find_all():
#         entry[j.name] = j.text.strip()

#     transaction_date = i.find("transactionDate")
#     for j in transaction_date.find_all():
#         entry[j.name] = j.text.strip()

#     transaction_coding = i.find("transactionCoding")
#     for j in transaction_coding.find_all():
#         entry[j.name] = j.text.strip()

#     transaction_amounts = i.find("transactionAmounts")
#     transaction_shares = transaction_amounts.find("transactionShares")
#     transaction_shares_value = transaction_shares.find("value")
#     entry["transactionShares"] = transaction_shares_value.text.strip()
#     transaction_price_per_share = transaction_amounts.find("transactionPricePerShare")
#     transaction_price_per_share_value = transaction_price_per_share.find("value")
#     entry["transactionPricePerShare"] = transaction_price_per_share_value.text.strip()
#     transaction_acquired_disposed_code = transaction_amounts.find("transactionAcquiredDisposedCode")
#     transaction_acquired_disposed_code_value = transaction_acquired_disposed_code.find("value")
#     entry["transactionAcquiredDisposedCode"] = transaction_acquired_disposed_code_value.text.strip()

#     post_transaction_amounts = i.find("postTransactionAmounts")
#     shares_owned_following_transaction = post_transaction_amounts.find("sharesOwnedFollowingTransaction")
#     shares_owned_following_transaction_value = shares_owned_following_transaction.find("value")
#     entry["sharesOwnedFollowingTransaction"] = shares_owned_following_transaction_value.text.strip()

#     ownership_nature = i.find("ownershipNature")
#     direct_or_indirect_ownership = ownership_nature.find("directOrIndirectOwnership")
#     direct_or_indirect_ownership_value = direct_or_indirect_ownership.find("value")
#     entry["directOrIndirectOwnership"] = direct_or_indirect_ownership_value.text.strip()
#     nature_of_ownership = ownership_nature.find("natureOfOwnership")
#     nature_of_ownership_value = nature_of_ownership.find("value")
#     entry["natureOfOwnership"] = nature_of_ownership_value.text.strip()


# for i in issuer_info_values:
#     entry[i[0]] = i[1]
# for i in reporting_owner_info_values:
#     entry[i[0]] = i[1]
# for i in reporting_owner_address_values:
#     entry[i[0]] = i[1]
# for i in reporting_owner_relationship_values:
#     entry[i[0]] = i[1]
# print(entry)
