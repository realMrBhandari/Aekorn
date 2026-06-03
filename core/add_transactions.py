# ! All input modules from core/input
from sql.insert_statement import append_transaction
from utilities import cli_input_helpers as help_input

# TODO [2]: fix function naming develop a pattern
# TODO [3]: FIX QUERIES REQUIRING COMMIT VS NON COMMIT


def log_transaction():
    # ?Basic Flow of programme:  [transaction amount] --> [type of transaction (income/expense?)] --> [transaction category] --> [transaction date] --> [transaction metadata (account, mode, node)]
    transaction_amount = help_input.amount_processor()

    transaction_type = help_input.transaction_side()

    transaction_category = help_input.map_transaction_category(int(transaction_type))

    transaction_date = help_input.ask_transaction_date()

    transaction_mode, transaction_account, transaction_note = (
        help_input.get_transaction_metadata()
    )  # ? this function returns tuple so unpacking tuple

    append_transaction(
        txn_date=transaction_date,
        txn_type="CREDIT" if transaction_type == "1" else "DEBIT",
        txn_amount=transaction_amount,
        txn_category=transaction_category,
        txn_account=transaction_account,
        txn_mode=transaction_mode,
        txn_note=transaction_note,
    )
