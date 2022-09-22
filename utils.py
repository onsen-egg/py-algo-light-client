import pickle
from base64 import b64decode

txn_merkle_leaf = "TL".encode()
merkle_array_node = "MA".encode()

def load(obj_file):
  with open(obj_file, "rb") as f:
    return pickle.load(f)

# computeTransactionLeaf receives the transaction ID and the signed transaction in block's hash, and computes
# the leaf of the vector commitment associated with the transaction.
# Parameters:
# transactionHash - the Sha256 hash of the canonical msgpack encoded transaction.
# stibHash - the Sha256 of the canonical msgpack encoded transaction as it's saved in the block.
def compute_transaction_leaf(
  transaction_hash, # 32 bytes
  stib_hash # 32 bytes
):
  pass

def verify_transaction(
  transaction_hash, # 32 bytes
  transaction_proof, # transactionProofResponse json dict thing
  lightblockheader_proof, # lightBlockHeaderProof json dict response thing
  confirmed_round, # number
  genesis_hash, # 32 bytes
  seed, # 32 bytes
  block_interval_commitment # 32 bytes
):
  stibhash = b64decode(transactionProof["stibhash"])