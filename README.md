# BitcoinScripting-

## Team Name : CryptoKnights 

### Team Members:

- *Janapareddy Vidya Varshini* - 230041013
- *Korubilli Vaishnavi* -  230041016
- *Mullapudi Namaswi* - 230041023

## Project Overview

This project demonstrates the creation and validation of Bitcoin transactions using:

1. *Legacy (P2PKH) Transactions*
2. *SegWit (P2SH-P2WPKH) Transactions*

We use *Bitcoin Core (bitcoind)* in regtest mode and Python scripts to interact with it via RPC calls. The project includes:

- Setting up a Bitcoin regtest network.
- Creating wallets and generating addresses.
- Funding transactions and analyzing scripts.
- Comparing transaction sizes between Legacy and SegWit formats.

---

## Prerequisites

### Install Dependencies

Ensure you have the following installed:

1. *Bitcoin Core* (bitcoind & bitcoin-cli): [Download Bitcoin Core](https://bitcoincore.org/en/download/)
2. *Python3* (if not installed, install via sudo apt install python3 or brew install python3)
3. *Required Python Libraries*<br>
   <strong>pip install python-bitcoinrpc</strong>
   

### Configure Bitcoin Core

1. Locate the bitcoin.conf file (usually found in ~/.bitcoin/bitcoin.conf on Linux/macOS or C:\Users\YourUser\AppData\Roaming\Bitcoin\bitcoin.conf on Windows).
2. Add the following configuration for regtest mode:<br>
   ini<br>
   regtest=1<br>
   server=1<br>
   rpcuser=your_rpc_user<br>
   rpcpassword=your_rpc_password<br>
   rpcport=18443<br>
   txindex=1<br>
   
3. Start bitcoind in regtest mode:
   
  <strong> bitcoind -regtest -daemon</strong>
   

---

## Running the Project

### Step 1: Start Bitcoin Daemon


<strong>bitcoind -regtest -daemon</strong>


### Step 2: Run the Legacy Transaction Script


<strong>python legacy_transactions.py</strong>

This will:

- Create a wallet<br>
- Generate addresses A, B, C<br>
- Fund address A<br>
- Create a transaction from A → B<br>
- Create a transaction from B → C<br>
- Decode and analyze transactions<br>

### Step 3: Run the SegWit Transaction Script


python segwit_transactions.py


This follows the same process as above but using P2SH-SegWit addresses.

### Step 4: Analyze Transactions

- Check decoded transactions in the output.<br>
- Use Bitcoin Debugger to verify script execution.<br>

---

## Expected Output

Upon running the scripts, you should see:

1. *Wallet and Address Creation*
2. *Transaction IDs for A → B and B → C*
3. *Decoded Scripts (locking & unlocking mechanisms)*
4. *Transaction size comparison between Legacy and SegWit*

---
