from bs4 import BeautifulSoup
import requests

class EdgarTxtFileParser():
    def __init__(self):
        self.headers = {
            "User-Agent": "Riley Martin rileymartin523@gmail.com",
        }

    def get_txt_file(self, txt_file_url):
        resp = requests.get(txt_file_url, headers=self.headers)
        return resp.text

    def parse_txt_file(self, text):
        xml_start = text.find("<?xml")
        xml_end = text.find("</XML>") + len("</XML>")
        xml_content = text[xml_start:xml_end]

        soup = BeautifulSoup(xml_content, "lxml-xml")
        doc = soup.find("ownershipDocument")

        def get_text(element, path):
            tag = element.find(path)
            return tag.text.strip() if tag and tag.text else ""

        header_info = {}
        for line in text.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                header_info[key.strip()] = val.strip()

        owner = doc.find("reportingOwner")
        owner_id = owner.find("reportingOwnerId")
        owner_address = owner.find("reportingOwnerAddress")

        issuer = doc.find("issuer")

        data = {
            "accessionNumber": header_info.get("ACCESSION NUMBER"),
            "formType": header_info.get("CONFORMED SUBMISSION TYPE"),
            "periodOfReport": header_info.get("CONFORMED PERIOD OF REPORT"),
            "filedAsOfDate": header_info.get("FILED AS OF DATE"),
            "reportingOwnerName": get_text(owner_id, "rptOwnerName"),
            "reportingOwnerCik": get_text(owner_id, "rptOwnerCik"),
            "reportingOwnerStreet1": get_text(owner_address, "rptOwnerStreet1"),
            "reportingOwnerStreet2": get_text(owner_address, "rptOwnerStreet2"),
            "reportingOwnerCity": get_text(owner_address, "rptOwnerCity"),
            "reportingOwnerState": get_text(owner_address, "rptOwnerState"),
            "reportingOwnerZip": get_text(owner_address, "rptOwnerZipCode"),
            "issuerName": get_text(issuer, "issuerName"),
            "issuerCik": get_text(issuer, "issuerCik"),
            "issuerSymbol": get_text(issuer, "issuerTradingSymbol"),
        }

        for i, txn in enumerate(doc.find_all("nonDerivativeTransaction"), 1):
            data[f"nonDerivative_{i}_securityTitle"] = get_text(txn, "securityTitle/value")
            data[f"nonDerivative_{i}_transactionDate"] = get_text(txn, "transactionDate/value")
            data[f"nonDerivative_{i}_transactionCode"] = get_text(txn, "transactionCoding/transactionCode")
            data[f"nonDerivative_{i}_shares"] = get_text(txn, "transactionAmounts/transactionShares/value")
            data[f"nonDerivative_{i}_price"] = get_text(txn, "transactionAmounts/transactionPricePerShare/value")
            data[f"nonDerivative_{i}_acquiredDisposedCode"] = get_text(txn, "transactionAmounts/transactionAcquiredDisposedCode/value")
            data[f"nonDerivative_{i}_sharesAfter"] = get_text(txn, "postTransactionAmounts/sharesOwnedFollowingTransaction/value")

        for i, txn in enumerate(doc.find_all("derivativeTransaction"), 1):
            data[f"derivative_{i}_securityTitle"] = get_text(txn, "securityTitle/value")
            data[f"derivative_{i}_transactionDate"] = get_text(txn, "transactionDate/value")
            data[f"derivative_{i}_transactionCode"] = get_text(txn, "transactionCoding/transactionCode")
            data[f"derivative_{i}_shares"] = get_text(txn, "transactionAmounts/transactionShares/value")
            data[f"derivative_{i}_price"] = get_text(txn, "transactionAmounts/transactionPricePerShare/value")
            data[f"derivative_{i}_acquiredDisposedCode"] = get_text(txn, "transactionAmounts/transactionAcquiredDisposedCode/value")
            data[f"derivative_{i}_underlyingSecurityTitle"] = get_text(txn, "underlyingSecurity/underlyingSecurityTitle/value")
            data[f"derivative_{i}_underlyingShares"] = get_text(txn, "underlyingSecurity/underlyingSecurityShares/value")
            data[f"derivative_{i}_sharesAfter"] = get_text(txn, "postTransactionAmounts/sharesOwnedFollowingTransaction/value")

        return data

