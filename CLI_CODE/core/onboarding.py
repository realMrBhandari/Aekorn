import sqlite3
from tabulate import tabulate
from utilities.cli_input_helpers import amount_processor


def start_Onboarding():
    connect = sqlite3.connect("database/FinCLI.db")
    cursor = connect.cursor()

    #!  executing all the schemas
    schemas = [
        "sql/schema/accounts.sql",
        "sql/schema/income_expense.sql",
        "sql/schema/obligations.sql",
        "sql/schema/people.sql",
        # "sql/schema/transactions.sql",
    ]
    for file_name in schemas:
        with open(file_name, "r") as file:
            cursor.executescript(file.read())

    connect.commit()

    #!   function to take bank account data and log it
    def get_bankAccount_input():
        account_name = input("Name of your bank: ")
        running_balance = amount_processor()
        with open("sql/insert/accounts.sql", "r") as file:
            cursor.execute(file.read(), (account_name, running_balance))

        connect.commit()

    #!  Onboarding screen message
    print(
        "\033[1;32mWelcome to FinCLI. Let's add your bank accounts and personalize your financial experience.\033[0m"
    )

    get_bankAccount_input()

    #! Decision for adding another bank account

    valid_responses = ["y", "yes", "n", "no"]

    while True:
        add_another_account = (
            input(
                "\n\033[33mWould you like to add another bank account? (y/n): \033[0m"
            )
            .strip()
            .lower()
        )

        while add_another_account not in valid_responses:
            print("\033[31mIncorrect input! Try again.\033[0m")
            add_another_account = (
                input(
                    "\n\033[33mWould you like to add another bank account? (y/n): \033[0m"
                )
                .strip()
                .lower()
            )

        if add_another_account in ["n", "no"]:
            break

        get_bankAccount_input()

    cursor.close()
    connect.close()
