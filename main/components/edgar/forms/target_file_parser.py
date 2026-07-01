import xml.etree.ElementTree as ET
from datetime import datetime

class TargetFileParser:
    def __init__(self):
        pass

    def get_txt_field(self, txt_file : str, field_name : str) -> str | None:
        for line in txt_file.splitlines():
            if line.startswith(field_name + ":"):
                value = line.split(":", 1)[1].strip()

                try:
                    return datetime.strptime(value, "%Y%m%d").date().isoformat()
                except ValueError:
                    return None

        return None
    
    def convert_txt_to_xml(self, txt_file : str) -> str | None:
        start_tag = "<XML>"
        end_tag = "</XML>"

        start = txt_file.find(start_tag)
        if start == -1:
            return None

        end = txt_file.find(end_tag, start)
        if end == -1:
            return None

        return txt_file[start + len(start_tag): end].strip()

    def parse_xml(self, xml_string : str) -> ET.Element | None:
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError as e:
            return None

    def get_text(self, element : ET.Element | None, path : str, default=None) -> str | None:
        if element is None:
            return default

        parts = path.split("/")
        for part in parts:
            element = element.find(part)
            if element is None:
                return default

        return element.text
    
    def parse_xml_by_parent_tag(self, xml_string : str, parent_tag_list : list[str]) -> dict[str, str | None] | None:
        root = self.parse_xml(xml_string)
        if root is None:
            return None

        info = {}

        for parent_tag in parent_tag_list:
            parent = root.find(parent_tag)

            if parent is None:
                return None

            for child in parent:
                info[child.tag] = child.text

        return info

    def parse_xml_non_derivative_table(self, xml_string : str) -> list[dict[str, str | None]]:
        root = self.parse_xml(xml_string)
        if root is None:
            return []

        table = root.find(".//nonDerivativeTable")
        if table is None:
            return []

        results = []

        for tx in table.findall("nonDerivativeTransaction"):
            results.append({
                "security_title": self.get_text(tx, "securityTitle/value"),
                "transaction_date": self.get_text(tx, "transactionDate/value"),
                "transaction_form_type": self.get_text(tx, "transactionCoding/transactionFormType"),
                "transaction_code": self.get_text(tx, "transactionCoding/transactionCode"),
                "equity_swap_involved": self.get_text(tx, "transactionCoding/equitySwapInvloved"),
                "transaction_shares": self.get_text(tx, "transactionAmounts/transactionShares/value"),
                "transaction_price_per_share": self.get_text(tx, "transactionAmounts/transactionPricePerShare/value"),
                "transaction_acquired_disposed_code": self.get_text(tx, "transactionAmounts/transactionAcquiredDisposedCode/value"),
                "shares_owned_following_transaction": self.get_text(tx, "postTransactionAmounts/sharesOwnedFollowingTransaction/value"),
                "ownershipNature": self.get_text(tx, "ownershipNature/directOrIndirectOwnership/value"),
            })

        return results