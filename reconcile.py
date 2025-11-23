import pandas as pd
from web3 import Web3

print("Script started")

# Connect to Ethereum Mainnet via Alchemy
rpc_url = "https://eth-mainnet.g.alchemy.com/v2/bFKMAFZDS9fNcSfTZemOn"
web3 = Web3(Web3.HTTPProvider(rpc_url))

print("Connected:", web3.is_connected())

# Load off-chain ledger
ledger = pd.read_csv("custody_ledger.csv")

# Pick the first transaction from ledger
ledger_tx = ledger.iloc[0].to_dict()
tx_hash = ledger_tx["tx_id"]

# Fetch on-chain transaction
try:
    onchain_tx = web3.eth.get_transaction(tx_hash)
except Exception as e:
    print(f"❌ Error fetching transaction: {e}")
    exit()

print("\nLedger entry:")
for k, v in ledger_tx.items():
    print(f"  {k}: {v}")

print("\nOn-chain transaction:")
print(f"  from:   {onchain_tx['from']}")
print(f"  to:     {onchain_tx['to']}")
print(f"  value:  {int(onchain_tx['value']) / 1e18:.6f} ETH")

# ETH reconciliation logic with dynamic tolerance
def reconcile_eth(ledger_tx, onchain_tx, tolerance_pct=0.5):
    ledger_from = ledger_tx["from"].lower()
    ledger_to = ledger_tx["to"].lower()
    ledger_amount = float(ledger_tx["amount"])
    onchain_from = onchain_tx["from"].lower()
    onchain_to = onchain_tx["to"].lower()
    onchain_amount = int(onchain_tx["value"]) / 1e18  # Convert wei to ETH

    # Calculate dynamic tolerance
    tolerance = ledger_amount * (tolerance_pct / 100)

    print("\n🔍 Reconciliation Check:")
    print(f"  Ledger from:     {ledger_from}")
    print(f"  On-chain from:   {onchain_from}")
    print(f"  Ledger to:       {ledger_to}")
    print(f"  On-chain to:     {onchain_to}")
    print(f"  Ledger amount:   {ledger_amount} ETH")
    print(f"  On-chain amount: {onchain_amount:.6f} ETH")
    print(f"  Tolerance:       ±{tolerance:.8f} ETH ({tolerance_pct}% of ledger amount)")

    if ledger_from == onchain_from and ledger_to == onchain_to and abs(ledger_amount - onchain_amount) <= tolerance:
        print("✅ Reconciliation successful")
    else:
        print("❌ Reconciliation failed")

# Run reconciliation with 0.5% tolerance
reconcile_eth(ledger_tx, onchain_tx, tolerance_pct=0.5)