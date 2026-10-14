from django import forms
from .models import (
    AekornUser,
    MoneyAccount,
    Transaction,
    IncomeExpenseCategory,
    IncomeExpenseRecord,
    Counterparty,
    ObligationRecord,
)


# ON-BOARDING & ADD ACCOUNT FORMS
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = AekornUser
        fields = ["akrn_user_name"]


class AccountRegistrationForm(forms.ModelForm):
    model = MoneyAccount
    fields = ["account_name", "account_category", "running_balance"]

    widgets = {
        "account_name": forms.TextInput(
            attrs={"placeholder": "e.g. American Express."}
        ),
        # "account_category":
        "running_balance": forms.NumberInput(attrs={"placeholder": "1.00", "min": "1"}),
    }


# ADD TRANSACTION FORMS
class TransactionRecordForm(forms.ModelForm):
    model = Transaction
    fields = ["txn_amt", "txn_account", "txn_date", "txn_type", "txn_note"]
    widgets = {
        "txn_amt": forms.NumberInput(attrs={"placeholder": "1.00", "min": "1"}),
        "txn_date": forms.DateInput(attrs={"type": "date"}),
        "txn_note": forms.TextInput(attrs={"placeholder": "e.g. hotwheels purchased"}),
    }


class IncomeExpenseTransactionForm(forms.ModelForm):
    model = IncomeExpenseRecord
    fields = ["category"]


class ObligationTransactionForm(forms.ModelForm):
    model = ObligationRecord
    fields = ["counterparty_name", "returned_amt"]
    widgets = {
        "returned_amt": forms.NumberInput(attrs={"placeholder": "1.00", "min": "1"})
    }


# TRANSACTION ADDITIONAL PARAMETERS FORM
class IncomeExpenseCategoryForm(forms.ModelForm):
    model = IncomeExpenseCategory
    fields = ["category_name", "category_type"]
    widgets = {
        "category_name": forms.TextInput(attrs={"placeholder": "e.g. Subscriptions"})
    }


class CounterpartyForm(forms.ModelForm):
    model = Counterparty
    fields = ["name", "relationship"]
    widgets = {
        "name": forms.TextInput(
            attrs={
                "placeholder": "e.g. John Doe",
            }
        ),
        "relationship": forms.TextInput(attrs={"placeholder": "e.g. Office Collegue"}),
    }
