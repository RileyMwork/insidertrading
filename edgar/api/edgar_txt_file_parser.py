import xml.etree.ElementTree as ET

class EdgarTxtFileParser:
    def __init__(self):
        pass

    def convert_txt_to_xml(self, txt_file):
        start_tag = "<XML>"
        end_tag = "</XML>"

        start = txt_file.find(start_tag)
        end = txt_file.find(end_tag)

        if start != -1 and end != -1:
            xml_string = txt_file[start + len(start_tag):end].strip()
            return xml_string
        
    def parse_xml_by_parent_tag(self, xml_string, parent_tag_list):
        info  = {}
        root = ET.fromstring(xml_string)

        for parent_tag in parent_tag_list:
            parent = root.find(parent_tag)
            if parent:
                for child in parent:
                    info[child.tag] = child.text
            else:
                print(f"Could Not Find Parent Tag {parent_tag}")
                return None

        return info
    
    def parse_xml_non_derivative_table(self, xml_string):
        root = ET.fromstring(xml_string)

        non_derivative_transaction_data = []

        non_derivative_transaction_table = root.find(".//nonDerivativeTable")
        if non_derivative_transaction_table is None:
            return []
        
        non_derivative_transactions_list = non_derivative_transaction_table.findall("nonDerivativeTransaction") 
        for transaction in non_derivative_transactions_list:
            non_derivative_transaction = {
                "security_title": transaction.findtext("securityTitle/value"),
                "transaction_date": transaction.findtext("transactionDate/value"),
                "transaction_form_type": transaction.findtext("transactionCoding/transactionFormType"),
                "transaction_code": transaction.findtext("transactionCoding/transactionCode"),
                "equity_swap_invloved": transaction.findtext("transactionCoding/equitySwapInvloved"),
                "transaction_shares": transaction.findtext("transactionAmounts/transactionShares/value"),
                "transaction_price_per_share": transaction.findtext("transactionAmounts/transactionPricePerShare/value"),
                "transaction_acquired_disposed_code": transaction.findtext("transactionAmounts/transactionAcquiredDisposedCode/value"),
                "shares_owned_following_transaction": transaction.findtext("postTransactionAmounts/sharesOwnedFollowingTransaction/value"),
                "ownershipNature": transaction.findtext("ownershipNature/directOrIndirectOwnership/value"),
            }

            non_derivative_transaction_data.append(non_derivative_transaction)

        return non_derivative_transaction_data