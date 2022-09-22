from utils import load
import algosdk
from algosdk.encoding import msgpack

state_proof = load("state_proof")
lightblockheader_proof = load("lightblockheader_proof")
tx_proof = load("transaction_proof")
