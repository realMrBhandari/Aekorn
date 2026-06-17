UPDATE accounts
SET running_balance = ?, modified_at = datetime('now')
WHERE account_id = ?