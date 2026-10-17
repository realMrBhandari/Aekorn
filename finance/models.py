import uuid
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


# ! ZONE 1: Transaction Classification that describe/classify transactions.
# Model for source categorization for income/expense
class IncomeExpenseSource(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=50)
    source_category = models.CharField(
        max_length=7,
        choices=[
            ("CREDIT", "Income Transaction"),
            ("DEBIT", "Expense Transaction"),
        ],
    )

    def __str__(self):
        return self.source_name


# Model for payment method for expense trasnctions
class PaymentMethod(models.Model):
    method_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=15)

    def __str__(self):
        return self.method_name


# Model for registering counterparty i.e. institutions / individuals with which lend/borrow transaction was performed
class Counterparty(models.Model):
    counterparty_id = models.BigAutoField(primary_key=True)
    counterparty_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.counterparty_name


# ! ZONE 2: Contains the actual financial domain
# Model stores the user profile associated with an Aekorn installation.
class AekornUser(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_name = models.CharField(max_length=100)
    onboarded_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-onboarded_on"]
        verbose_name = "User"
        verbose_name_plural = "Users"


# Model represents a financial account or money-holding account tracked in Aekorn.
class MoneyAccount(models.Model):
    user_id = models.ForeignKey(AekornUser, on_delete=models.CASCADE)
    account_id = models.BigAutoField(primary_key=True)
    account_name = models.CharField(max_length=100)
    account_category = models.CharField(
        max_length=10,
        choices=[
            ("SALARY", "Salary Account"),
            ("SAVINGS", "Savings Account"),
            ("CURRENT", "Current Account"),
            ("CASH", "Money Pot"),
            ("WALLET", "Digital Wallet"),
        ],
    )
    running_balance = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    registred_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        ordering = [
            "-registred_on",
        ]

    def __str__(self):
        return self.account_name


# Model for Base Transaction, contains the fields common to all transaction types.
class Transaction(models.Model):
    txn_id = models.BigAutoField(primary_key=True)
    txn_amt = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    txn_account = models.ForeignKey(MoneyAccount, on_delete=models.RESTRICT)
    txn_date = models.DateField()
    txn_category = models.CharField(
        max_length=13,
        choices=[
            ("CREDIT", "Income Transaction"),
            ("DEBIT", "Expense Transaction"),
            ("SELF_TRANSFER", "Self Transfer"),
            ("LEND", "Lent Money"),
            ("BORROW", "Borrowed Money"),
            ("INVESTMENT", "Investment"),
        ],
    )
    txn_note = models.CharField(max_length=50, blank=True)
    is_visible = models.BooleanField(default=True)
    recorded_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-txn_date", "-txn_id"]


# model extending Base Transction with income/expense specific information
class IncomeExpenseRecord(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    base_txn = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    source = models.ForeignKey(IncomeExpenseSource, on_delete=models.PROTECT)

    class Meta:
        ordering = [
            "-base_txn__txn_date",
            "-base_txn__txn_id",
        ]


# model extending Expense Transaction with payment method metadata
class ExpensePaymentMethod(models.Model):
    expense_payment_id = models.BigAutoField(primary_key=True)
    expense_id = models.OneToOneField(
        IncomeExpenseRecord,
        on_delete=models.CASCADE,
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
    )


# model extending Base Transction with money lent/borrowed information
class ObligationRecord(models.Model):
    base_txn = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    counterparty_name = models.ForeignKey(Counterparty, on_delete=models.PROTECT)
    returned_amt = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_obligation_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)

    # if is_obligation_active == False: updated_on will be trated as closure date
    class Meta:
        ordering = [
            "-base_txn__txn_date",
            "-base_txn__txn_id",
        ]
