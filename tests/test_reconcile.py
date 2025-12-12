# tests/test_reconcile.py
import pandas as pd
import pytest

# Import your reconciliation function from reconcile.py
# Adjust the import if your function name or file structure differs
from reconcile import compare_balances

# --- Sanity check to confirm pytest is working ---
def test_sanity_check():
    assert 1 + 1 == 2

# --- Example test using hardcoded ETH balances ---
def test_eth_balance_match():
    ledger = {"ETH": 1.0}
    chain = {"ETH": 1.0}
    assert compare_balances(ledger, chain) is True

def test_eth_balance_mismatch():
    ledger = {"ETH": 1.0}
    chain = {"ETH": 0.9}
    assert compare_balances(ledger, chain) is False

# --- Example test using your custody_ledger.csv ---
def test_csv_reconciliation():
    # Load sample ledger balances from CSV
    df = pd.read_csv("custody_ledger.csv")

    # Assume CSV has columns: token, ledger_balance, chain_balance
    for _, row in df.iterrows():
        ledger = {row["token"]: row["ledger_balance"]}
        chain = {row["token"]: row["chain_balance"]}

        # Call your reconciliation function
        result = compare_balances(ledger, chain)

        # Assert based on tolerance logic (adjust if you allow small differences)
        if row["ledger_balance"] == row["chain_balance"]:
            assert result is True
        else:
            assert result is False