import sqlite3
from tabulate import tabulate


def calculate_all_accountBalance():
    connect = sqlite3.connect("database/fincil.db")
    cursor = connect.cursor()
    cursor.execute("""SELECT SUM(running_balance) FROM accounts""")
    net_balance = cursor.fetchall()
    cursor.close()
    connect.close()
    return net_balance


def get_individual_accounts():
    connect = sqlite3.connect("database/fincil.db")
    cursor = connect.cursor()
    cursor.execute(""" SELECT bank_account_name, running_balance FROM accounts;""")
    individual_accounts = cursor.fetchall()
    cursor.close()
    connect.close()
    return individual_accounts
