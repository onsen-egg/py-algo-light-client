import sys
from utils import AssetLoader, verify_transaction

# In CLI run: python3 main.py <ASSET_FOLDER_NAME>

if __name__ == '__main__':
  if len(sys.argv) == 1:
    raise Exception('Provide a folder containing the proof assets as an argument')

  assets = AssetLoader(sys.argv[1])

  result = verify_transaction(
    assets.tx_hash,
    assets.tx_proof,
    assets.lightblockheader_proof,
    assets.round_number,
    assets.genesis_hash,
    assets.seed,
    assets.block_interval_commitment
  )

  assert(result)
