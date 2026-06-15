from ..db_connect import DbConnect

class SQLSetup(DbConnect):
    def __init__(self):
        super().__init__()

    def create_edgar_insider_transactions_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insider_transactions (
                issuerCik VARCHAR(20),
                issuerName VARCHAR(255),
                issuerTradingSymbol VARCHAR(20),
                issuerForeignTradingSymbol VARCHAR(20),
        
                rptOwnerCik VARCHAR(20),
                rptOwnerName VARCHAR(255),
                rptOwnerNonUSAddressFlag BOOLEAN,
                rptOwnerStreet1 VARCHAR(255),
                rptOwnerStreet2 VARCHAR(255),
                rptOwnerCity VARCHAR(100),
                rptOwnerState VARCHAR(50),
                rptOwnerZipCode VARCHAR(20),
                rptOwnerStateDescription VARCHAR(100),
        
                isDirector BOOLEAN,
                isOfficer BOOLEAN,
                isTenPercentOwner BOOLEAN,
                isOther BOOLEAN,
                officerTitle VARCHAR(255),
        
                security_title VARCHAR(100),
                transaction_date DATE,
                transaction_form_type VARCHAR(10),
                transaction_code VARCHAR(5),
                equity_swap_invloved VARCHAR(5),
        
                transaction_shares DECIMAL(20,4),
                transaction_price_per_share DECIMAL(20,4),
                total_transaction_cost DECIMAL(20,4),
                transaction_acquired_disposed_code VARCHAR(5),
        
                shares_owned_following_transaction DECIMAL(20,4),
                ownershipNature VARCHAR(10),
        
                rptOwnerNonUSStateTerritory VARCHAR(50),
                rptOwnerCountry VARCHAR(50),
                otherText VARCHAR(255),
        
                date_pulled_from_edgar DATE,
        
                sic INTEGER,
                industry VARCHAR(255)
            );
        """)
        conn.commit()