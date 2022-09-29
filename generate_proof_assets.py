import sys
from proofAssets import generate_proof_assets

# In CLI run: python3 generate_proof_assets.py <FOLDER_NAME> <NETWORK>
# <NETWORK> is optional, can be mainnet or testnet

if __name__ == '__main__':
  if len(sys.argv) > 2:
    generate_proof_assets(sys.argv[1], sys.argv[2])
  else:
    generate_proof_assets(sys.argv[1])
