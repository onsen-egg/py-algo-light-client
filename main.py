from utils import AssetLoader, verify_transaction

asset_folder = 'testing'

assets = AssetLoader(asset_folder)

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
