# ! THIS FILE DEALS WITH RECORDING ALL THE TRANSACTIONS IN FINCLI, NOTHING ELSE OTHER THAN TRANSACTIONS OR TRASNACTION HELPERS SHOULD BE HERE

import sqlite3
from dev.db_queries import QueryHandler


class BaseTransaction:
    # todo add validations using property methods
    def __init__(self, amt, date):
        self.transaction_amount = amt
        self.trasnaction_date = date


class IncomeLogger(BaseTransaction):
    def __init__(self, amt, date, account, category, note):
        super().__init__(amt, date)
        self.transaction_account = account
        self.income_category = category
        self.transaction_note = note

    def calculate_new_balance(self):
        current_balance = QueryHandler.get_individual_balance(self.transaction_account)
        return current_balance + self.transaction_amount

    def update_database(self):
        connection = sqlite3.connect("database/FinCLI.db")
        cursor = connection.cursor()
        QueryHandler.update_account_balance(
            cursor, self.transaction_account, self.calculate_new_balance()
        )
        QueryHandler.log_income_transaction(
            self.transaction_amount,
            self.trasnaction_date,
            self.income_category,
            self.transaction_account,
            self.transaction_note,
            cursor,
        )
        connection.commit()
        cursor.close()
        connection.close()
        # maybe some code here to send a message to frontend that it's a sucess
