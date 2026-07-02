from utilities import cli_input_helpers as helper
from transactions.income_expense import log_self_transfer_transaction


def add_transaction():
    transaction_amt = helper.amount_processor()
    transaction_date = helper.ask_transaction_date()
    log_self_transfer_transaction(transaction_amt)
