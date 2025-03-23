# Bitcoin Scripting Assignment

## CS 216: Introduction to Blockchain

### Assignment 3: Bitcoin Scripting    

## Team Members:

- **Name 1** (Roll Number 1)
- **Name 2** (Roll Number 2)
- **Name 3** (Roll Number 3)

## Project Overview

This project demonstrates the creation and validation of Bitcoin transactions using:

1. **Legacy (P2PKH) Transactions**
2. **SegWit (P2SH-P2WPKH) Transactions**

We use **Bitcoin Core (bitcoind)** in regtest mode and Python scripts to interact with it via RPC calls. The project includes:

- Setting up a Bitcoin regtest network.
- Creating wallets and generating addresses.
- Funding transactions and analyzing scripts.
- Comparing transaction sizes between Legacy and SegWit formats.

---

## Prerequisites

### Install Dependencies

Ensure you have the following installed:

1. **Bitcoin Core** (bitcoind & bitcoin-cli): [Download Bitcoin Core](https://bitcoincore.org/en/download/)
2. **Python3** (if not installed, install via `sudo apt install python3` or `brew install python3`)
3. **Required Python Libraries**
   ```sh
   pip install python-bitcoinrpc
   ```

### Configure Bitcoin Core

1. Locate the `bitcoin.conf` file (usually found in `~/.bitcoin/bitcoin.conf` on Linux/macOS or `C:\Users\YourUser\AppData\Roaming\Bitcoin\bitcoin.conf` on Windows).
2. Add the following configuration for regtest mode:
   ```ini
   regtest=1
   server=1
   rpcuser=your_rpc_user
   rpcpassword=your_rpc_password
   rpcport=18443
   txindex=1
   ```
3. Start bitcoind in regtest mode:
   ```sh
   bitcoind -regtest -daemon
   ```

---

## Running the Project

### Step 1: Start Bitcoin Daemon

```sh
bitcoind -regtest -daemon
```

### Step 2: Run the Legacy Transaction Script

```sh
python legacy_transactions.py
```

This will:

- Create a wallet
- Generate addresses A, B, C
- Fund address A
- Create a transaction from A → B
- Create a transaction from B → C
- Decode and analyze transactions

### Step 3: Run the SegWit Transaction Script

```sh
python segwit_transactions.py
```

This follows the same process as above but using P2SH-SegWit addresses.

### Step 4: Analyze Transactions

- Check decoded transactions in the output.
- Use Bitcoin Debugger to verify script execution.

---

## Expected Output

Upon running the scripts, you should see:

1. **Wallet and Address Creation**
2. **Transaction IDs for A → B and B → C**
3. **Decoded Scripts (locking & unlocking mechanisms)**
4. **Transaction size comparison between Legacy and SegWit**

---

## Submission Details

- **GitHub Repository:** [Your Repo Link]
- **Report:** Attached in the repository with screenshots and analysis.

For any issues, refer to [Bitcoin Command Line Guide](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line/blob/master/18_0_Talking_to_Bitcoind_Other.md).

