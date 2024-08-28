import json
import sys
import logging
from substrateinterface import SubstrateInterface, Keypair
from getpass import getpass
from pathlib import Path

# Load configuration
config = {
    "nodeWS": "wss://rpc.devolvedai.com/rpc",
    "denom": "AGC",
    "decimalPlaces": 18,
    "validator": "GTzRQPzkcuynHgkEHhsPBFpKdh4sAacVRsnd8vYfPpTMeEY",
    "validators": [
        "GTzRQPzkcuynHgkEHhsPBFpKdh4sAacVRsnd8vYfPpTMeEY",
        "EPStAMtjApGg8Ap6xKe9gyuinjmetz1MNhzu1cPmLQkWKUA",
        "DSpbbk6HKKyS78c4KDLSxCetqbwnsemv2iocVXwNe2FAvWC",
        "DSA55HQ9uGHE5MyMouE8Geasi2tsDcu3oHR4aFkJ3VBjZG5",
        "J4XkgJjMP6c1pqneV5KogJvJLM1qReXP9SAMJt33prnDdwB",
    ],
    "password": "",
    "accountJSON": "./account.json",
    "log": True,
}

# Configure logging
# logging.basicConfig(filename="autopayout.log", level=logging.INFO)

def load_account_json(filepath):
    try:
        with open(filepath, 'r') as file:
            account_data = json.load(file)
            print("Account JSON loaded successfully.")
            return account_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading account JSON: {e}")
        sys.exit(1)

def main():
    print("\nArgochain Auto Payout")
    print("- Made with love from The Devolved AI Team  https://devolvedai.com/\n")

    # Load account
    account_data = load_account_json(config["accountJSON"])

    # Ensure that the required keys are present
    if "encoded" not in account_data or "address" not in account_data:
        print("Invalid account JSON structure.")
        sys.exit(1)

    address = account_data['address']
    print(f"Account address: {address}")

    password = config['password'] or getpass(f"Enter password for {address}: ")

    try:
        # Create Keypair from JSON
        keypair = Keypair.create_from_encrypted_json(account_data, password)
        print("Keypair created successfully.")
    except Exception as e:
        print(f"Failed to decode the keypair: {e}")
        sys.exit(1)

    print("Attempting to connect to Argochain node...")
    substrate = SubstrateInterface(
        url=config["nodeWS"],
        ss58_format=2,
        type_registry_preset='kusama'
    )
    print("Connected to the node successfully.")

    account_info = substrate.query('System', 'Account', [address])
    print(f"Account info: {account_info}")
    
    # Correctly handle the balance conversion
    available_balance = int(account_info['data']['free'].value)

    if available_balance <= 0:
        print(f"Account {address} doesn't have available funds")
        sys.exit(1)

    print(f"Account {address} available balance is {available_balance}")
    logging.info(f"Account {address} available balance is {available_balance}")

    active_era = substrate.query('Staking', 'ActiveEra')['index']
    logging.info(f"Active era is {active_era}")

    for validator in config["validators"]:
        # Attempt to retrieve staking info for the validator
        staking_info = substrate.query('Staking', 'Validators', [validator])
        print(f"Staking info for validator {validator}: {staking_info}")
        
        # Print the type and structure of staking_info for inspection
        print(f"Type of staking_info: {type(staking_info)}")
        print(f"Staking info details: {staking_info}")
        logging.info(f"Staking info for validator {validator}: {staking_info}")

        # Check if 'claimed_rewards' key exists in the staking info
        if 'claimed_rewards' in staking_info:
            claimed_rewards = staking_info['claimed_rewards']
            logging.info(f"Claimed eras for validator {validator}: {claimed_rewards}")
        else:
            print(f"'claimed_rewards' key not found in staking_info. Available details: {staking_info}")
            logging.info(f"'claimed_rewards' key not found in staking_info. Available details: {staking_info}")
            continue  # Skip to the next validator if 'claimed_rewards' is not found

        transactions = []

        for era in range(max(0, active_era - 84), active_era):
            if era not in claimed_rewards:
                transactions.append(
                    substrate.compose_call(
                        call_module='Staking',
                        call_function='payout_stakers',
                        call_params={
                            'validator_stash': validator,
                            'era': era
                        }
                    )
                )

        if transactions:
            extrinsic = substrate.create_signed_extrinsic(
                call=substrate.compose_call(
                    call_module='Utility',
                    call_function='batch',
                    call_params={'calls': transactions}
                ),
                keypair=keypair
            )

            try:
                receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
                logging.info(f"Success! Check tx in PolkaScan: https://polkascan.io/kusama/transaction/{receipt.extrinsic_hash}")
            except Exception as e:
                logging.error(f"Failed to submit extrinsic: {e}")
                sys.exit(1)
        else:
            logging.info(f"No unclaimed rewards for validator {validator}")

if __name__ == "__main__":
    main()
