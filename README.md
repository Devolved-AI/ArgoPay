## ArgoPay

### Argochain Auto Payout Tool - User Documentation

#### Overview

The Argochain Auto Payout Tool is designed to help validators on the Argochain network automate the process of claiming staking rewards. The tool connects to the Argochain node via WebSocket and uses an encrypted JSON keystore to sign and submit transactions that claim rewards.

#### Prerequisites

Before using the Auto Payout Tool, ensure you have the following:

1. **Python 3.7+ installed** on your machine.
2. **Required Python packages installed:**
   - Install necessary packages by running:
     ```bash
     pip install substrate-interface
     ```

3. **Account JSON File:**
   - You need an `account.json` file that contains your encrypted account details.

#### Setting Up

1. **Create the `account.json` File**

   The `account.json` file contains your account's encrypted keypair and metadata. You can export this from your wallet (e.g., Polkadot.js extension).

   Here’s an example structure for `account.json`:

   ```json
   {
     "encoded": "YOUR_ENCODED_KEYPAIR_HERE",
     "address": "YOUR_ACCOUNT_ADDRESS_HERE",
     "encoding": {
       "content": ["pkcs8", "ed25519"],
       "type": "scrypt",
       "version": "2"
     },
     "meta": {
       "name": "Your Account Name",
       "tags": [],
       "whenCreated": 1639659091000
     }
   }
   ```

   - Replace `YOUR_ENCODED_KEYPAIR_HERE` with your actual encoded keypair.
   - Replace `YOUR_ACCOUNT_ADDRESS_HERE` with your actual account address.

2. **Ensure Configuration is Correct**

   The script uses a configuration dictionary within the code. Here’s an example configuration:

   ```python
   config = {
       "nodeWS": "wss://rpc.devolvedai.com/",
       "denom": "AGC",
       "decimalPlaces": 18,
       "validator": "GTzRQPzkcuynHgkEHhsPBFpKdh4sAacVRsnd8vYfPpTMeEY",
       "validators": [
           "GTzRQPzkcuynHgkEHhsPBFpKdh4sAacVRsnd8vYfPpTMeEY",
           "EPStAMtjApGg8Ap6xKe9gyuinjmetz1MNhzu1cPmLQkWKUA",
           "DSpbbk6HKKyS78c4KDLSxCetqbwnsemv2iocVXwNe2FAvWC",
           "DSA55HQ9uGHE5MyMouE8Geasi2tsDcu3oHR4aFkJ3VBjZG5",
           "J4XkgJjMP6c1pqneV5KogJvJLM1qReXP9SAMJt33prnDdwB"
       ],
       "password": "",
       "accountJSON": "./account.json",
       "log": True,
   }
   ```

   - **nodeWS**: The WebSocket URL for the Argochain node.
   - **denom**: The denomination of the token (e.g., `AGC`).
   - **decimalPlaces**: The number of decimal places for the token.
   - **validator**: The main validator address.
   - **validators**: A list of validator addresses to claim rewards for.
   - **password**: The password for decrypting the JSON keystore (optional).
   - **accountJSON**: The path to your `account.json` file.
   - **log**: Whether to log actions to `autopayout.log`.

#### Running the Script

1. **Execute the Script**

   After setting up the `account.json` file and verifying the configuration, run the script by executing the following command:

   ```bash
   python autopayout.py
   ```

   - The script will prompt you for the password if it’s not provided in the configuration.

2. **Script Output**

   - The script will display your account address and connect to the Argochain node.
   - It will then retrieve your account balance and check for available funds.
   - The script will automatically check for unclaimed rewards across the specified validators and submit transactions to claim them.
   - All actions and any errors encountered will be logged to `autopayout.log`.

#### Logging

The script logs all actions to `autopayout.log` by default. This includes information about transactions, any errors that occur, and other relevant details.

#### Troubleshooting

- **Invalid Account JSON Structure:** Ensure your `account.json` file is correctly formatted and includes both `encoded` and `address` keys.
- **Connection Issues:** Verify that the WebSocket URL is correct and that your internet connection is stable.
- **Insufficient Funds:** Ensure your account has enough funds to cover transaction fees.

#### Security Considerations

- **Keep your `account.json` secure.** This file contains sensitive information that could allow someone to access your account.
- **Use strong passwords.** If your keystore is encrypted with a password, make sure it’s strong and not easily guessable.

#### Conclusion

The Argochain Auto Payout Tool simplifies the process of managing validator rewards on the Argochain network. By automating payouts, it helps ensure that you efficiently collect your staking rewards without missing any opportunities. If you encounter any issues or need further assistance, feel free to contact the Devolved AI support team.

For more information, visit [Devolved AI](https://devolvedai.com/).
