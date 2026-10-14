import uuid
from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class AekornUser(models.Model):
    akrn_user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    akrn_user_name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)


class MoneyAccount(models.Model):
    user_id = models.ForeignKey(AekornUser, on_delete=models.CASCADE)
    account_id = models.BigAutoField(primary_key=True)
    account_name = models.CharField(max_length=100)
    account_category = models.CharField(max_length=10)
    running_balance = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(1)]
    )
    registred_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


# class TransactionCategories(models.TextChoices):
#     # todo learn enum and move all the choice fields as an enum field || For numeric based choices we will use IntegerChoices, and for character ones we will use TextChoices
#     pass


class Transaction(models.Model):
    txn_id = models.BigAutoField(primary_key=True)
    txn_amt = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(1)]
    )
    txn_account = models.ForeignKey(MoneyAccount, on_delete=models.RESTRICT)
    txn_date = models.DateField()
    txn_type = models.CharField(
        max_length=13,
        choices=[
            ("CREDIT", "Income"),
            ("DEBIT", "Expense"),
            ("SELF_TRANSFER", "Self Transfer"),
            ("LEND", "Lend"),
            ("BORROW", "Borrow"),
            ("INVESTMENT", "Investment"),
        ],
    )
    txn_note = models.CharField(max_length=50, null=True, blank=True)
    # is visible will be responsible for showing user the trasnaction in case user deletes the transction, the transaction will be hidden from the ui and an equal reverse trasnaction will be performed which will also be hidden from the ui while keeping history intact
    is_visible = models.BooleanField(default=True)
    recorded_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)


class IncomeExpenseCategory(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    category_type = models.CharField(
        max_length=7,
        choices=[
            ("CREDIT", "Income"),
            ("DEBIT", "Expense"),
        ],
    )


class IncomeExpenseRecord(models.Model):
    base_transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeExpenseCategory, on_delete=models.PROTECT)


class Counterparty(models.Model):
    counterparty_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)


class ObligationRecord(models.Model):
    base_transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    counterparty_name = models.ForeignKey(Counterparty, on_delete=models.PROTECT)
    returned_amt = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00, validators=[MinValueValidator(1)]
    )
    # pending_amt = models.DecimalField(max_digits=15, decimal_places=2) WILL DERIVE PENDING AMOUNT USING BUSINESS LOGIC
    is_obligation_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    # if is_obligation_active == False: updated_on will be trated as closure date
