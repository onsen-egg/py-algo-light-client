from utils import AssetLoader, verify_transaction, load

asset_folder = 'testassets1'

assets = AssetLoader(asset_folder)

verify_transaction(
  assets.tx_hash,
  assets.tx_proof,
  assets.lightblockheader_proof,
  assets.round_number,
  assets.genesis_hash,
  assets.seed,
  assets.block_interval_commitment
)

# state_proof = load("state_proof")
# lightblockheader_proof = load("lightblockheader_proof")
# tx_proof = load("transaction_proof")
# block_info = load("block_info")
# tx_hash_b64 = load("tx_hash_b64")

# verify_transaction(
#   b64decode(tx_hash_b64),
#   tx_proof,
#   lightblockheader_proof,
#   block_info['rnd'],
#   b64decode(block_info['gh']),
#   b64decode(block_info['seed']),
#   b64decode(state_proof['Message']['BlockHeadersCommitment'])
# )
