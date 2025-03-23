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
wallet_name = "Crypto_Knights"

# Check existing wallets
try:
    wallets = rpc_connection.listwallets()
    print(f"Existing Wallets: {wallets}")

    if wallet_name in wallets:
        print(f"Wallet '{wallet_name}' is already loaded.")
    else:
        # Check if the wallet exists on the filesystem but is not loaded
        wallet_path = f"C:\\Users\\Namaswi\\AppData\\Roaming\\Bitcoin\\regtest\\wallets\\{wallet_name}"
        if os.path.exists(wallet_path):
            print(f"Wallet '{wallet_name}' exists on the filesystem but is not loaded.")
            print("Attempting to load the wallet...")
            try:
                rpc_connection.loadwallet(wallet_name)
                print(f"Wallet '{wallet_name}' loaded successfully.")
            except Exception as load_error:
                print(f"Error loading wallet '{wallet_name}': {load_error}")
                print("The wallet may be corrupted. Deleting and recreating the wallet...")
                # Delete the corrupted wallet folder
                shutil.rmtree(wallet_path)
                print(f"Deleted wallet folder: {wallet_path}")
                # Recreate the wallet
                rpc_connection.createwallet(wallet_name)
                print(f"Wallet '{wallet_name}' created successfully.")
        else:
            # Create the wallet if it doesn't exist
            print(f"Wallet '{wallet_name}' does not exist. Creating it...")
            rpc_connection.createwallet(wallet_name)
            print(f"Wallet '{wallet_name}' created successfully.")
except Exception as e:
    print(f"Error with wallet: {e}")
    exit()

# Create a new RPC connection for the wallet
try:
    rpc_connection_wallet = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}")
    print(f"Connected to wallet '{wallet_name}' successfully.")
except Exception as e:
    print(f"Error connecting to wallet '{wallet_name}': {e}")
    exit()

# Generate three legacy addresses
try:
    address_A = rpc_connection_wallet.getnewaddress("", "legacy")
    address_B = rpc_connection_wallet.getnewaddress("", "legacy")
    address_C = rpc_connection_wallet.getnewaddress("", "legacy")
    print(f"Address A: {address_A}")
    print(f"Address B: {address_B}")
    print(f"Address C: {address_C}")

    # Save addresses to a file
    addresses = {
        "address_A": address_A,
        "address_B": address_B,
        "address_C": address_C
    }
    with open("addresses.json", "w") as f:
        json.dump(addresses, f)
    print("Addresses saved to addresses.json")
except Exception as e:
    print(f"Error generating addresses: {e}")
    exit()

# Fund Address A by mining blocks
try:
    rpc_connection.generatetoaddress(101, address_A)
    print(f"101 blocks mined to Address A: {address_A}")
except Exception as e:
    print(f"Error mining blocks: {e}")
    exit()

# Create a transaction from Address A to Address B
try:
    # Get the unspent transaction output (UTXO) for Address A
    unspent_A = rpc_connection_wallet.listunspent(0, 9999999, [address_A])
    if not unspent_A:
        print("No unspent transactions found for Address A.")
        exit()

    # Check the value of the UTXO
    utxo_value = unspent_A[0]['amount']
    print(f"UTXO Value: {utxo_value} BTC")

    # Dynamic fee calculation using estimatesmartfee
    conf_target = 6  # Aim for confirmation within 6 blocks
    fee_estimates = rpc_connection.estimatesmartfee(conf_target)

    if "errors" in fee_estimates or "feerate" not in fee_estimates:
        print("Error estimating fee. Using fallback fee rate.")
        fee_rate = Decimal("0.00001")  # Lower fallback fee rate in BTC/kB
    else:
        fee_rate = Decimal(str(fee_estimates["feerate"]))  # Fee rate in BTC/kB

    tx_size = Decimal("200")  # Approximate transaction size in bytes
    fee = fee_rate * (tx_size / Decimal("1000"))  # Calculate fee in BTC

    # Ensure the UTXO value is greater than the fee
    if utxo_value <= fee:
        print(f"UTXO value ({utxo_value} BTC) is too small to cover the fee ({fee} BTC).")
        print("Mining more blocks to fund Address A...")
        rpc_connection.generatetoaddress(1, address_A)  # Mine 1 more block
        print("1 block mined. Address A should now have a UTXO.")
        unspent_A = rpc_connection_wallet.listunspent(0, 9999999, [address_A])
        utxo_value = unspent_A[0]['amount']
        print(f"Updated UTXO Value: {utxo_value} BTC")

    output_amount = utxo_value - fee  # Subtract the fee
    print(f"Sending {output_amount} BTC to Address B (Fee: {fee} BTC)")

    # Create a raw transaction
    raw_tx_A_to_B = rpc_connection_wallet.createrawtransaction(
        [{"txid": unspent_A[0]['txid'], "vout": unspent_A[0]['vout']}],
        {address_B: float(output_amount)}  # Convert Decimal to float for RPC
    )
    print(f"Raw Transaction (A to B): {raw_tx_A_to_B}")

    # Sign the transaction
    signed_tx_A_to_B = rpc_connection_wallet.signrawtransactionwithwallet(raw_tx_A_to_B)
    print(f"Signed Transaction (A to B): {signed_tx_A_to_B}")

    # Broadcast the transaction
    txid_A_to_B = rpc_connection_wallet.sendrawtransaction(signed_tx_A_to_B['hex'])
    print(f"Transaction ID (A to B): {txid_A_to_B}")

    # Decode the raw transaction (A to B)
    decoded_tx_A_to_B = rpc_connection_wallet.decoderawtransaction(raw_tx_A_to_B)
    print(f"Decoded Transaction (A to B): {decoded_tx_A_to_B}")

    # Extract the ScriptPubKey for Address B
    scriptPubKey_B = decoded_tx_A_to_B['vout'][0]['scriptPubKey']['hex']
    print(f"ScriptPubKey for Address B: {scriptPubKey_B}")

except Exception as e:
    print(f"Error creating transaction (A to B): {e}")
    exit()
