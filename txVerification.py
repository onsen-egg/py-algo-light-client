from base64 import b64decode
from hashlib import sha256
from utils import serialize_light_block_header

txn_merkle_leaf = "TL".encode()
merkle_array_node = "MA".encode()

lightblockheader_prefix = "B256".encode()

left_child = 0
right_child = 1

# computeTransactionLeaf receives the transaction ID and the signed transaction in block's hash, and computes
# the leaf of the vector commitment associated with the transaction.
# Parameters:
# transactionHash - the Sha256 hash of the canonical msgpack encoded transaction.
# stibHash - the Sha256 of the canonical msgpack encoded transaction as it's saved in the block.
def compute_transaction_leaf(
  transaction_hash: bytes, # 32 bytes
  stib_hash: bytes # 32 bytes
) -> bytes:
  m = sha256()
  m.update(txn_merkle_leaf + transaction_hash + stib_hash)
  # The leaf returned is of the form: Sha256("TL" || Sha256(transaction) || Sha256(transaction in block))
  return m.digest()

def compute_lightblockheader_leaf(
  round_number, # uint64
  transaction_commitment, # 32 bytes
  genesis_hash, # 32 bytes
  seed # 32
):
  lbh_serialized = serialize_light_block_header(
    seed,
    genesis_hash,
    round_number,
    transaction_commitment
  )

  m = sha256()
  m.update(lightblockheader_prefix + lbh_serialized)
  return m.digest()

# SOLIDITY NOTE: gas inefficient (needless memory usage)
def get_vector_commitment_positions(
  leaf_index: int, # uint64
  tree_depth: int, # uint64
  ) -> "list[int]":
  if tree_depth == 0:
    raise Exception("ErrInvalidTreeDepth")
  
  if leaf_index >= 1<<tree_depth:
    raise Exception("ErrIndexDepthMismatch")
  
  directions = [0] * tree_depth
  
  for i in reversed(range(len(directions))):
    directions[i] = leaf_index & 1
    leaf_index >>= 1
  
  return directions

def compute_vector_commitment_root(
  leaf: bytes, # 32 bytes
  leaf_index: int, # uint64
  proof: bytes, # bytes
  tree_depth: int, # uint64
) -> bytes:
  if len(proof) == 0 and tree_depth == 0:
    return leaf

  node_hash_size = sha256().digest_size

  if tree_depth * node_hash_size != len(proof):
    raise Exception("ErrProofLengthTreeDepthMismatch")
  
  positions = get_vector_commitment_positions(
    leaf_index,
    tree_depth
  )

  current_node = leaf

  for distance_from_leaf in range(tree_depth):
    sibling_index_in_proof = distance_from_leaf * node_hash_size
    sibling_hash = proof[sibling_index_in_proof : sibling_index_in_proof + node_hash_size]

    node_domain_separator = merkle_array_node
    internal_node_data = node_domain_separator

    if positions[distance_from_leaf] == left_child:
      internal_node_data += current_node + sibling_hash
    else:
      internal_node_data += sibling_hash + current_node
    
    m = sha256()
    m.update(internal_node_data)
    current_node = m.digest()
  
  return current_node

def verify_transaction(
  transaction_hash, # 32 bytes
  transaction_proof, # transactionProofResponse json dict thing
  lightblockheader_proof, # lightBlockHeaderProof json dict response thing
  confirmed_round, # uint64
  genesis_hash, # 32 bytes
  seed, # 32 bytes
  block_interval_commitment # 32 bytes
) -> bool:
  if transaction_proof['hashtype'] != "sha256":
    raise Exception("Only sha256 is supported for hashtype")

  stib_hash = b64decode(transaction_proof["stibhash"])

  transaction_leaf = compute_transaction_leaf(
    transaction_hash, 
    stib_hash
  )
  print("transaction_leaf: 0x{}".format(transaction_leaf.hex()))

  transaction_proof_root = compute_vector_commitment_root(
    transaction_leaf,
    transaction_proof['idx'],
    b64decode(transaction_proof['proof']),
    transaction_proof['treedepth']
  )
  print("transaction_proof_root: 0x{}".format(transaction_proof_root.hex()))

  candidate_lightblockheader_leaf = compute_lightblockheader_leaf(
    confirmed_round,
    transaction_proof_root,
    genesis_hash,
    seed
  )

  lightblockheader_proof_root = compute_vector_commitment_root(
    candidate_lightblockheader_leaf,
    lightblockheader_proof['index'],
    b64decode(lightblockheader_proof['proof']),
    lightblockheader_proof['treedepth']
  )
  print("lightblockheader_proof_root: 0x{}".format(lightblockheader_proof_root.hex()))
  print("block_interval_commitment: 0x{}".format(block_interval_commitment.hex()))

  return lightblockheader_proof_root == block_interval_commitment
