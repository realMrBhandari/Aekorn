UPDATE accounts
SET running_balance = ?, modified_at = datetime('now','localtime')
WHERE account_id = ?