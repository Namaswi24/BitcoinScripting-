from bitcoinrpc.authproxy import AuthServiceProxy
import json
from decimal import Decimal

# RPC credentials
rpc_user = "Namaswi"
rpc_password = "Namaswi"
rpc_port = 18443  # Use 18443 for regtest mode
wallet_name = "Crypto_Knights"

# Connect to the wallet-specific RPC endpoint
try:
    rpc_connection_wallet = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}")
    print(f"Connected to wallet '{wallet_name}' successfully.")
except Exception as e:
    print(f"Error connecting to wallet '{wallet_name}': {e}")
    exit()

# Load addresses from the file
try:
    with open("addresses.json", "r") as f:
        addresses = json.load(f)
    address_B = addresses["address_B"]
    address_C = addresses["address_C"]
    print(f"Address B: {address_B}")
    print(f"Address C: {address_C}")
except Exception as e:
    print(f"Error loading addresses: {e}")
    exit()

# Get the unspent transaction output (UTXO) for Address B
try:
    unspent_B = rpc_connection_wallet.listunspent(0, 9999999, [address_B])
    if not unspent_B:
        print("No unspent transactions found for Address B. Funding Address B...")
        rpc_connection_wallet.generatetoaddress(101, address_B)  # Mine 101 blocks to make the reward spendable
        print("101 blocks mined. Address B should now have a UTXO.")
        unspent_B = rpc_connection_wallet.listunspent(0, 9999999, [address_B])
        print("Updated UTXOs for Address B:", unspent_B)

    # Check the value of the UTXO
    utxo_value_B = unspent_B[0]['amount']
    print(f"UTXO Value (B): {utxo_value_B} BTC")

    # Dynamic fee calculation using estimatesmartfee
    conf_target = 6  # Aim for confirmation within 6 blocks
    fee_estimates = rpc_connection_wallet.estimatesmartfee(conf_target)

    if "errors" in fee_estimates or "feerate" not in fee_estimates:
        print("Error estimating fee. Using fallback fee rate.")
        fee_rate = Decimal("0.0002")  # Fallback fee rate in BTC/kB
    else:
        fee_rate = Decimal(str(fee_estimates["feerate"]))  # Fee rate in BTC/kB

    tx_size = Decimal("200")  # Approximate transaction size in bytes
    fee = fee_rate * (tx_size / Decimal("1000"))  # Calculate fee in BTC
    output_amount_B_to_C = utxo_value_B - fee  # Subtract the fee
    print(f"Sending {output_amount_B_to_C} BTC to Address C (Fee: {fee} BTC)")

    # Create a raw transaction
    raw_tx_B_to_C = rpc_connection_wallet.createrawtransaction(
        [{"txid": unspent_B[0]['txid'], "vout": unspent_B[0]['vout']}],
        {address_C: float(output_amount_B_to_C)}  # Convert Decimal to float for RPC
    )
    print(f"Raw Transaction (B to C): {raw_tx_B_to_C}")

    # Sign the transaction
    signed_tx_B_to_C = rpc_connection_wallet.signrawtransactionwithwallet(raw_tx_B_to_C)
    print(f"Signed Transaction (B to C): {signed_tx_B_to_C}")

    # Broadcast the transaction
    try:
        txid_B_to_C = rpc_connection_wallet.sendrawtransaction(signed_tx_B_to_C['hex'])
        print(f"Transaction ID (B to C): {txid_B_to_C}")

        # Decode the raw transaction (B to C)
        decoded_tx_B_to_C = rpc_connection_wallet.decoderawtransaction(signed_tx_B_to_C['hex'])
        print(f"Decoded Transaction (B to C): {decoded_tx_B_to_C}")

        # Extract the ScriptSig and ScriptPubKey
        scriptSig = decoded_tx_B_to_C['vin'][0]['scriptSig']['hex']
        scriptPubKey_C = decoded_tx_B_to_C['vout'][0]['scriptPubKey']['hex']
        print(f"ScriptSig: {scriptSig}")
        print(f"ScriptPubKey for Address C: {scriptPubKey_C}")

        # Get the ScriptPubKey from the previous transaction (A to B)
        txid_A_to_B = unspent_B[0]['txid']
        try:
            # Try to get the transaction using getrawtransaction
            decoded_tx_A_to_B = rpc_connection_wallet.getrawtransaction(txid_A_to_B, True)
        except Exception as e:
            # If getrawtransaction fails, try gettransaction (for wallet transactions)
            print(f"Error getting raw transaction: {e}. Trying gettransaction...")
            decoded_tx_A_to_B = rpc_connection_wallet.gettransaction(txid_A_to_B)

        scriptPubKey_B = decoded_tx_A_to_B['vout'][unspent_B[0]['vout']]['scriptPubKey']['hex']
        print(f"ScriptPubKey from previous transaction (A to B): {scriptPubKey_B}")

    except Exception as e:
        print(f"Error broadcasting or decoding transaction (B to C): {e}")

except Exception as e:
    print(f"Error creating transaction (B to C): {e}")
