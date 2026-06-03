from tabulate import tabulate
from sql.fetching_data import fetch_All_tranasctions

# ? tabulate specific formatting


def display_transactions():
    print(
        tabulate(
            fetch_All_tranasctions(),
            headers=[
                "Date",
                "Type",
                "Amt",
                "Category",
                "Mode",
                "Account",
                "Description",
            ],
            tablefmt="heavy_grid",
        )
    )
