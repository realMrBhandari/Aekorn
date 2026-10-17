from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import (
    AekornUser,
    MoneyAccount,
    Transaction,
    IncomeExpenseSource,
    IncomeExpenseRecord,
    PaymentMethod,
    ExpensePaymentMethod,
    Counterparty,
    ObligationRecord,
)

from datetime import date


# ON-BOARDING & ADD ACCOUNT FORMS
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = AekornUser
        fields = ["user_name"]
        widgets = {
            "user_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. John Doe",
                    "id": "user-name",
                    "class": "input",
                }
            )
        }


class AddMoneyAccountForm(forms.ModelForm):
    running_balance = forms.DecimalField(
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(
            attrs={
                "placeholder": "e.g. 1.00",
                "min": "0.01",
                "class": "input",
                "id": "running-balance",
            }
        ),
    )

    class Meta:
        model = MoneyAccount
        fields = ["account_name", "account_category", "running_balance"]

        widgets = {
            "account_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. American Express.",
                    "class": "input",
                    "id": "account-name",
                }
            ),
            "account_category": forms.Select(
                attrs={
                    "class": "select",
                    "id": "account-type",
                }
            ),
        }


# ADD TRANSACTION FORMS
class LogTransactionForm(forms.ModelForm):
    txn_amt = forms.DecimalField(
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(
            attrs={
                "placeholder": "e.g. 1.00",
                "min": "0.01",
                "class": "input",
                "id": "amount-field",
                "hx-target": "#select-txn-account",
                "hx-trigger": "blur",
                "hx-swap": "outerHTML",
            }
        ),
    )
    txn_date = forms.DateField(
        validators=[MaxValueValidator(date.today())],
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "input",
                "max": f"{date.today().strftime('%Y-%m-%d')}",
                "id": "transaction-date",
            }
        ),
    )

    class Meta:
        model = Transaction
        fields = ["txn_amt", "txn_account", "txn_date", "txn_category", "txn_note"]
        widgets = {
            "txn_account": forms.Select(
                attrs={
                    "class": "select",
                    "id": "transaction-account",
                    "hx-trigger": "change",
                    "hx-target": "#select-txn-type",
                    "hx-swap": "outerHTML",
                }
            ),
            "txn_category": forms.Select(
                attrs={
                    "class": "select",
                    "id": "transaction-type",
                    "hx-get": "/transaction/extend",
                    "hx-target": "#form-extension",
                    "hx-trigger": "change",
                    "hx-swap": "innerHTML",
                    "hx-include": "#transaction-account",
                }
            ),
            "txn_note": forms.Textarea(
                attrs={
                    "placeholder": "e.g. Amazon Prime renewal",
                    "class": "textarea",
                    "id": "transaction-note",
                }
            ),
        }


class AddIncomeExpenseSourceForm(forms.ModelForm):
    class Meta:
        model = IncomeExpenseSource
        fields = ["source_name", "source_category"]
        widgets = {
            "source_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Subscriptions",
                    "class": "input",
                    "id": "source-name",
                }
            ),
            "source_category": forms.Select(
                attrs={"class": "select", "id": "source-category"}
            ),
        }


class AttachIncomeExpenseSourceForm(forms.ModelForm):
    class Meta:
        model = IncomeExpenseRecord
        fields = ["source"]
        widgets = {
            "source": forms.Select(
                attrs={"class": "select", "id": "transaction-source"}
            )
        }


class AddExpensePaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ["method_name"]
        widgets = {
            "method_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Online Transaction",
                    "class": "input",
                    "id": "payment-method-name",
                }
            )
        }


class AttachExpensePaymentMethodForm(forms.ModelForm):
    class Meta:
        model = ExpensePaymentMethod
        fields = ["payment_method"]
        widgets = {
            "payment_method": forms.Select(
                attrs={"class": "select", "id": "payment-method"}
            )
        }


class AddCounterpartyForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = ["counterparty_name", "relationship"]
        widgets = {
            "counterparty_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. John Doe",
                    "class": "input",
                    "id": "counterparty-name",
                }
            ),
            "relationship": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Office Collegue",
                    "class": "input",
                    "id": "counterparty-relationship",
                }
            ),
        }


class AttachObligationDataForm(forms.ModelForm):
    returned_amt = forms.DecimalField(validators=[MinValueValidator(0.01)])

    class Meta:
        model = ObligationRecord
        fields = ["counterparty_name", "returned_amt"]
        widgets = {
            "counterparty_name": forms.Select(
                attrs={"class": "select", "id": "counter-party"}
            ),
            "returned_amt": forms.NumberInput(
                attrs={"placeholder": "1.00", "min": "0.01", "class": "input"}
            ),
        }
