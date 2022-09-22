from utils import load, verify_transaction
import algosdk
from algosdk.encoding import msgpack
from base64 import b64decode

state_proof = load("state_proof")
lightblockheader_proof = load("lightblockheader_proof")
tx_proof = load("transaction_proof")
block_info = load("block_info")
tx_hash_b64 = load("tx_hash_b64")

verify_transaction(
  b64decode(tx_hash_b64),
  tx_proof,
  lightblockheader_proof,
  block_info['rnd'],
  b64decode(block_info['gh']),
  b64decode(block_info['seed']),
  b64decode(state_proof['Message']['BlockHeadersCommitment'])
)