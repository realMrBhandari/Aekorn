# ! THIS FILE DEALS WITH RECORDING ALL THE TRANSACTIONS IN FINCLI, NOTHING ELSE OTHER THAN TRANSACTIONS OR TRASNACTION HELPERS SHOULD BE HERE

import sqlite3
from dev.db_queries import QueryHandler


class BaseTransaction:
    #! todo add validations using property methods
    def __init__(self, amt, date, description):
        self.transaction_amount = amt
        self.trasnaction_date = date
        self.transaction_description = description


class IncomeTransactionLogger(BaseTransaction):
    def __init__(self, amt, date, description, account, category):
        super().__init__(amt, date, description)
        self.transaction_account = account
        self.income_category = category

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
            self.transaction_description,
            cursor,
        )
        connection.commit()
        cursor.close()
        connection.close()
        # maybe some code here to send a message to frontend that it's a sucess


class ExpenseTrasnactionLogger(BaseTransaction):
    def __init__(self, amt, date, description, account, category, pay_mode):
        super().__init__(amt, date, description)
        #! todo: add account balance validation i.e. txn_Amount cannot be greater than txn_Account balance
        self.transaction_account = account
        self.expense_category = category
        self.payment_mode = pay_mode

    def calc_updated_balance(self):
        current_balance = QueryHandler.get_individual_balance(self.transaction_account)
        return current_balance - self.transaction_amount

    def record_in_database(self):
        connection = sqlite3.connect("database/FinCLI.db")
        cursor = connection.cursor()
        QueryHandler.update_account_balance(
            cursor, self.transaction_account, self.calc_updated_balance()
        )
        QueryHandler.log_expense_transaction(
            self.transaction_amount,
            self.trasnaction_date,
            self.expense_category,
            self.transaction_account,
            self.transaction_description,
            cursor,
        )
        connection.commit()
        cursor.close()
        connection.close()
        # maybe some code here to send a message to frontend that it's a sucess


class SelfTransferLogger(BaseTransaction):
    def __init__(self, amt, date, description, src_ac, dest_ac):
        super().__init__(amt, date, description)
        self.source_account = src_ac
        self.destination_account = dest_ac

    def calc_updated_balance(self, account_side, operation):
        fetched_running_balance = QueryHandler.get_individual_balance(account_side)
        if operation == "DEDUCTION":
            return fetched_running_balance - self.transaction_amount
        elif operation == "ADDITION":
            return fetched_running_balance + self.transaction_amount

    def post_to_database(self):
        connection = sqlite3.connect("database/FinCLI.db")
        cursor = connection.cursor()
        # one update for source account
        QueryHandler.update_account_balance(
            cursor,
            self.source_account,
            self.calc_updated_balance(
                account_side=self.source_account, operation="DEDUCTION"
            ),
        )
        # one update for destination account
        QueryHandler.update_account_balance(
            cursor,
            self.destination_account,
            self.calc_updated_balance(
                account_side=self.destination_account, operation="ADDITION"
            ),
        )
        #! 2 more query here for trasnaction table to log trasnaction events i.e one dedcution from source account and one addition to destination account
        connection.commit()
        cursor.close()
        connection.close()


class LendTransactionLogger(BaseTransaction):
    pass


class BorrowTransactionLogger(BaseTransaction):
    pass


class ReturnTransactionLogger(BaseTransaction):
    pass
