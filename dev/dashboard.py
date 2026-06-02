from tabulate import tabulate
import sql.account_summary as account_overview
import database.fetching_data as fetch


def FinCLI_Dashboard():
    print(
        tabulate(
            [
                (
                    "\033[1;36mNet Account Balance:\033[0m",
                    account_overview.calculate_all_accountBalance(),
                )
            ],
            tablefmt="heavy_grid",
        )
    )

    print("\n\033[1;36mMy Accounts\033[0m")
    print(
        tabulate(
            (account_overview.get_individual_accounts()),
            headers=["Account Name", "Running Balance"],
            tablefmt="heavy_grid",
        )
    )

    print("\n\033[1;36m Recent Transactions\033[0m")
    print(
        tabulate(
            ((fetch.fetch__Recent_tranasctions())),
            headers=("TYPE", "AMOUNT", "PAYMENT METHOD", "CATEGORY", "DATE"),
            tablefmt="heavy_grid",
        ),
    )
