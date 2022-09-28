Implementation of transaction proof verification against a trusted block interval commitment.

Verification is in pure Python and implements all the necessary low-level logic, should be portable to any environment that has sha256.

To verify a transaction proof:
- `python3 main.py <PROOF_ASSETS_FOLDER>` e.g. `python3 main.py test_assets_1`

- Proof is valid if program runs with no exceptions. 

To generate the assets for a new state/tx proof:
- First install Algorand dependencies: `conda env create -f environment.yml` then `conda activate algorand`

- `python3 generate_proof_assets.py <NEW_FOLDER_NAME>`