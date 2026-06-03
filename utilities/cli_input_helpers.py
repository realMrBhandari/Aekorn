from utilities.amount_validator import isItFloat
from datetime import datetime, date
import calendar

red = "\033[31m"
green = "\033[32m"
reset = "\033[0m"


# //============================================================================================================================================================================================================


## this function deals with processing validating input amount
def amount_processor():

    input_amt = input("Please input amount: ")

    # ? Short circuit is preventing programme from crashing here.
    while (not isItFloat(input_amt)) or float(input_amt) <= 0:

        if not isItFloat(input_amt):
            print(f"{red}Your input {input_amt} is not a number{reset}.")
        elif float(input_amt) <= 0:
            print(f"{red}Your input {input_amt} is equal to 0{reset}.")

        input_amt = input("Please input amount: ")

    amt_normalized = round(float(input_amt), 2)
    return amt_normalized


# //============================================================================================================================================================================================================


def transaction_side():
    txn_type = input(
        "Specify the type of transaction\n"
        "[1] Income transaction\n"
        "[2] Expense transaction\n"
        "Choose an appropriate option 1 - 2: "
    )

    while not txn_type.isdigit() or txn_type not in ["1", "2"]:
        print("\033[31mInvalid input. Try again!\033[0m")
        txn_type = input("Choose an appropriate option 1 - 2: ")

    # ! UI to be handled seprately in future updates
    (
        print(
            "\033[1;32m ========================== Income Transaction Recording ==========================\033[0m\n"
        )
        if txn_type == "1"
        else print(
            "\033[1;31m ========================== Expense Transaction Recording ==========================\033[0m\n"
        )
    )

    return txn_type


# //============================================================================================================================================================================================================


## this function deals with mapping amunt to category
def map_transaction_category(choice):
    # ! NOTE: choice is that value which decides what transaction it is, if choice == 1 then it is income transaction else it is expense transction since we have binary logic here either it is income or it is expense, but I believe invalidating user inputs so for expense the choice value will be 2, but anyways any value which is not 1 will be considered as expense which is not the case as my previous step will never allow it
    # ? category data is stored in dictionaries allowing us to remove or edit categories in future should I implement an oboarding screen
    category_income = {
        1: "Business",
        2: "Freelancing",
        3: "Monthy Salary",
        4: "Bonus",
        4: "Pocket Money",
        5: "Others",
    }

    category_expense = {
        1: "Housing & Rent",
        2: "Loans & EMIs",
        3: "Investments",
        4: "Food & Groceries",
        5: "Transportation",
        6: "Bill & Utilities",
        7: "Health Care",
        8: "Shopping",
        9: "Education & Learning",
        10: "Travel & Hotel Bookings",
        11: "Entertainment",
        12: "Miscellaneous",
    }

    # ? prompting user for category message based on argument using ternary operator
    print(
        "Please Select Your Income Source"
        if choice == 1
        else "Where Was This Money Spent?"
    )

    #  making use of ternary operator to decide which dictionary to pick and ampping it to the argument provided so we don't have to use multiple if else statements in the code just to decide which dictionary to pick, making code shorter and honour DRY Principle
    map_category = category_income if choice == 1 else category_expense

    #  using for loop to extract keys and values from rhe dicitonary and printing them serially like a menu of choices, making use of .items() on dictionary mapped to the choice dictionary method and unpacking tupleusinf key, value in for loop
    for key, value in map_category.items():
        print(f"[{key}] {value}")

    # ? Prompting user to pick a transaction category as well as validating user inputs
    category_selection = input(
        f"Input your choice of category 1- {len(map_category)}: "
    )
    while (
        not category_selection.isdigit() or int(category_selection) not in map_category
    ):
        print(f"{red}Invalid selection. Try again!{reset}")
        category_selection = input(
            f"Input your choice of category 1- {len(map_category)}: "
        )

    # ? the transction category will be retruned back to the caller
    return map_category[int(category_selection)]


# //============================================================================================================================================================================================================

## transaction date mapping module

red = "\033[31m"
reset = "\033[0m"


def print_invalid():
    print(f"{red}Attention User! Invalid Input, try again!{reset}")


def get_valid_input(prompt, validator, error_message=None):
    value = input(prompt).strip()

    while not validator(value):
        if error_message:
            print(error_message)
        else:
            print_invalid()

        value = input(prompt).strip()

    return value


def is_valid_year(year):
    current_year = datetime.now().year

    return year.isnumeric() and len(year) == 4 and 2000 <= int(year) <= current_year


def is_valid_month(month, max_month):
    return month.isnumeric() and 1 <= int(month) <= max_month


def is_valid_day(day, max_day):
    return day.isnumeric() and 1 <= int(day) <= max_day


def ask_transaction_date():
    print("""\nWhen did this transaction occur?
 [1] Today 
 [2] Earlier this month
 [3] A specific date\n""")

    user_input = get_valid_input(
        "Please provide an option: ",
        lambda x: x in ["1", "2", "3"],
        f"{red}Attention User! Invalid Input, try again! {reset}",
    )

    # Option 1 → Today's date
    if user_input == "1":
        return datetime.now().date().strftime("%Y-%m-%d")

    # Option 2 → Earlier this month
    if user_input == "2":
        current_day = date.today().day

        def earlier_date_validator(x):
            if not x.isnumeric():
                print(f"{red}Invalid Input! {x} is not a number!{reset}")
                return False

            if int(x) > current_day:
                print(f"{red}Provided date {x} exceeds current date{reset}")
                return False

            return True

        earlier_date = get_valid_input(
            "Please provide transaction date: ",
            earlier_date_validator,
        )

        return f"{datetime.now().strftime('%Y-%m')}-{earlier_date.zfill(2)}"

    # Option 3 → Specific date
    current_date = datetime.now().date()
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day

    print(
        f"\033[33m*Numeric: Can only record YEAR between 2000 and {current_year}\033[0m"
    )

    transaction_date_year = get_valid_input(
        "Transaction YEAR: ",
        is_valid_year,
    )

    transaction_year = int(transaction_date_year)

    # Month validation
    if transaction_year == current_year:
        max_month = current_month

        print(
            f"\033[33m*Numeric: Can only record MONTH between 1 and current month({current_month})\033[0m"
        )
    else:
        max_month = 12

        print("\033[33m*Numeric: Can only record MONTH between 1 and 12\033[0m")

    transaction_date_month = get_valid_input(
        f"Transaction MONTH for year {transaction_date_year}: ",
        lambda x: is_valid_month(x, max_month),
    )

    transaction_month = int(transaction_date_month)

    # Day validation
    if transaction_year == current_year and transaction_month == current_month:
        max_day = current_day

        print(
            f"\033[33m*Numeric: Can only record DAY between 1 and {current_day}\033[0m"
        )
    else:
        max_day = calendar.monthrange(
            transaction_year,
            transaction_month,
        )[1]

        print(f"\033[33m*Numeric: Can only record DAY between 1 and {max_day}\033[0m")

    transaction_date_day = get_valid_input(
        "Transaction DAY: ",
        lambda x: is_valid_day(x, max_day),
    )

    return (
        f"{transaction_date_year}-"
        f"{transaction_date_month.zfill(2)}-"
        f"{transaction_date_day.zfill(2)}"
    )


# //============================================================================================================================================================================================================
# ? transaction bank_Account
def get_transaction_metadata():
    metadata = {}
    # ? transaction mode
    transaction_mode = (
        input("\nEnter transaction mode (e.g., Cash, Card, UPI) [max 20 chars]: \t")
        or "-"
    )
    while not len(transaction_mode) <= 20:
        transaction_mode = (
            input(
                "\n\033[31mInvalid input. Enter transaction mode (1–20 characters, e.g., Cash, Card, UPI):\033[0m "
            )
            or "—"
        )
    # ? account
    transaction_bank_account = (
        input(
            "\nEnter the account in which the income was credited(20 characters max):\t"
        )
        or "bank"
    )
    while not len(transaction_bank_account) <= 20:
        print()
        transaction_bank_account = (
            input(
                "\n\033[31mAccount name must be 1–20 characters. Enter the account where income was credited:\033[0m "
            )
            or "bank"
        )
    # ? transaction note
    transaction_note = input(
        "\nAdd a note to describe your transaction (50 characters max): "
    )
    while len(transaction_note) > 50 or len(transaction_note) < 1:
        print(
            "\033[31mInvalid Input! Note should be between 1 to 50 characters long, try again!\033[0m"
        )
        transaction_note = input("Add a note to describe your transaction: ")

    return transaction_mode, transaction_bank_account, transaction_note


# //============================================================================================================================================================================================================
