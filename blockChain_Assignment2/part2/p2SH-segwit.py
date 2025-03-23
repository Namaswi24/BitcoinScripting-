from bitcoinrpc.authproxy import AuthServiceProxy
import json
from decimal import Decimal
import os
import shutil

# RPC credentials
rpc_user = "Namaswi"
rpc_password = "Namaswi"
rpc_port = 18443  # Use 18443 for regtest mode

# Connect to bitcoind
try:
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")
    print("Connected to bitcoind successfully.")
except Exception as e:
    print(f"Error connecting to bitcoind: {e}")
    exit()

# Wallet name
wallet_name = "Crypto_Knights_2"

# Check existing wallets and load or create the wallet
try:
    wallets = rpc_connection.listwallets()
    if wallet_name not in wallets:
        print(f"Wallet '{wallet_name}' not found. Creating it...")
        rpc_connection.createwallet(wallet_name)
    rpc_connection_wallet = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}")
    print(f"Connected to wallet '{wallet_name}' successfully.")
except Exception as e:
    print(f"Error with wallet: {e}")
    exit()

# Generate three P2SH-SegWit addresses (A', B', C')
try:
    address_A = rpc_connection_wallet.getnewaddress("", "p2sh-segwit")
    address_B = rpc_connection_wallet.getnewaddress("", "p2sh-segwit")
    address_C = rpc_connection_wallet.getnewaddress("", "p2sh-segwit")
    print(f"P2SH-SegWit Address A: {address_A}")
    print(f"P2SH-SegWit Address B: {address_B}")
    print(f"P2SH-SegWit Address C: {address_C}")

    # Save addresses to a file
    addresses = {
        "address_A": address_A,
        "address_B": address_B,
        "address_C": address_C
    }
    with open("addresses_p2sh-segwit.json", "w") as f:
        json.dump(addresses, f)
    print("Addresses saved to addresses_p2sh-segwit.json")
except Exception as e:
    print(f"Error generating P2SH-SegWit addresses: {e}")
    exit()

# Fund Address A by mining blocks
try:
    rpc_connection.generatetoaddress(101, address_A)
    print(f"101 blocks mined to Address A: {address_A}")
except Exception as e:
    print(f"Error mining blocks: {e}")
    exit()

# Create a transaction from Address A' to Address B'
try:
    # Get the unspent transaction output (UTXO) for Address A
    unspent_A = rpc_connection_wallet.listunspent(0, 9999999, [address_A])
    utxo_value = unspent_A[0]['amount']
    print(f"UTXO Value (A): {utxo_value} BTC")

    # Calculate transaction fee
    conf_target = 6
    fee_estimates = rpc_connection.estimatesmartfee(conf_target)
    fee_rate = Decimal(str(fee_estimates["feerate"])) if "feerate" in fee_estimates else Decimal("0.00001")
    tx_size = Decimal("200")
    fee = fee_rate * (tx_size / Decimal("1000"))

    # Output amount after fee deduction
    output_amount = utxo_value - fee

    # Create a raw transaction
    raw_tx_A_to_B = rpc_connection_wallet.createrawtransaction(
        [{"txid": unspent_A[0]['txid'], "vout": unspent_A[0]['vout']}],
        {address_B: float(output_amount)}
    )

    # Sign the transaction
    signed_tx_A_to_B = rpc_connection_wallet.signrawtransactionwithwallet(raw_tx_A_to_B)
    txid_A_to_B = rpc_connection_wallet.sendrawtransaction(signed_tx_A_to_B['hex'])
    print(f"Transaction ID (A to B): {txid_A_to_B}")

    # Decode the transaction
    decoded_tx_A_to_B = rpc_connection_wallet.decoderawtransaction(raw_tx_A_to_B)
    print(f"Decoded Transaction (A to B): {decoded_tx_A_to_B}")

except Exception as e:
    print(f"Error creating transaction (A to B): {e}")
    exit()

# Create a transaction from Address B' to Address C'
try:
    # Get the unspent transaction output (UTXO) for Address B
    unspent_B = rpc_connection_wallet.listunspent(0, 9999999, [address_B])
    utxo_value_B = unspent_B[0]['amount']
    print(f"UTXO Value (B): {utxo_value_B} BTC")

    # Output amount after fee deduction
    output_amount_B = utxo_value_B - fee

    # Create a raw transaction
    raw_tx_B_to_C = rpc_connection_wallet.createrawtransaction(
        [{"txid": unspent_B[0]['txid'], "vout": unspent_B[0]['vout']}],
        {address_C: float(output_amount_B)}
    )

    # Sign the transaction
    signed_tx_B_to_C = rpc_connection_wallet.signrawtransactionwithwallet(raw_tx_B_to_C)
    txid_B_to_C = rpc_connection_wallet.sendrawtransaction(signed_tx_B_to_C['hex'])
    print(f"Transaction ID (B to C): {txid_B_to_C}")

    # Decode the transaction
    decoded_tx_B_to_C = rpc_connection_wallet.decoderawtransaction(raw_tx_B_to_C)
    print(f"Decoded Transaction (B to C): {decoded_tx_B_to_C}")

    # Extract ScriptPubKey for Address C
    scriptPubKey_C = decoded_tx_B_to_C['vout'][0]['scriptPubKey']['hex']
    print(f"ScriptPubKey for Address C: {scriptPubKey_C}")

except Exception as e:
    print(f"Error creating transaction (B to C): {e}")
    exit()
