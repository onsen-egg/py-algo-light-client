Implementation of transaction proof verification against a trusted block interval commitment.

Verification is in pure Python, fetching proofs from an Algo node requires py-algorand-sdk

To check a transaction proof:

`python3 main.py <PROOF_ASSETS_FOLDER>` e.g. `python3 main.py test_assets_1`

To generate the assets for a new state/tx proof:

`python3 generate_proof_assets.py <NEW_FOLDER_NAME>`