import sqlite3
from tabulate import tabulate
from utilities.cli_input_helpers import amount_processor

# ? Making connection with database
connect = sqlite3.connect("database/fincil.db")
cursor = connect.cursor()

# ? accounts table schema execution
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_account_name TEXT NOT NULL,
    running_balance REAL NOT NULL,
    recorded_on TEXT DEFAULT(datetime('now')) NOT NULL)
""")
connect.commit()

# ? Onboarding screen message
print(
    "\033[1;32mWelcome to FinCLI. Let's add your bank accounts and personalize your financial experience.\033[0m"
)


# ?  function to take bank account data and log it
def get_bankAccount_input():
    account_name = input("Name of your bank: ")
    running_balance = amount_processor()
    cursor.execute(f"""INSERT INTO accounts
                   (bank_account_name, running_balance)
                   VALUES
                   ("{account_name}", "{running_balance}");""")
    connect.commit()


get_bankAccount_input()

# ? Decision for adding another bank account
add_another_account = input(
    "\n\033[33mWould you like to add another bank account? (y/n): \033[0m"
)
valid_responses = [
    "y",
    "Y",
    "YES",
    "Yes",
    "yes",
    "n",
    "N",
    "NO",
    "No",
    "no",
]
while add_another_account not in valid_responses:
    print("\033[31m Incorrect input! Try again\033[0m")
    add_another_account = input(
        "\n\033[33mWould you like to add another bank account? (y/n): \033[0m"
    )

while add_another_account in ["y", "Y", "YES", "Yes", "yes"]:
    get_bankAccount_input()
    add_another_account = input(
        "\n\033[33mWould you like to add another bank account? (y/n): \033[0m"
    )
    valid_responses = [
        "y",
        "Y",
        "YES",
        "Yes",
        "yes",
        "n",
        "N",
        "NO",
        "No",
        "no",
    ]
    while add_another_account not in valid_responses:
        print("\033[31m Incorrect input! Try again\033[0m")


# ? Fetching logged data from db
def fetch_all_bankAccount_info():
    cursor.execute("SELECT * FROM accounts")
    accounts_info = cursor.fetchall()
    return accounts_info


print(
    tabulate(
        ((fetch_all_bankAccount_info())),
        headers=["Account ID", "Account Name", "Current Balance", "Recorded ON"],
        tablefmt="heavy_grid",
    )
)

cursor.close()
connect.close()
