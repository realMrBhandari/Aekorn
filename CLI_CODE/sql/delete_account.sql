UPDATE accounts
SET account_status = 'REMOVED', modified_at = datetime('now')
WHERE account_id = ?