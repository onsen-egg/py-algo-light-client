from hashlib import sha256
from utils import serialize_state_proof_message
from base64 import b64decode

strength_target = 256

state_proof_message_prefix = "spm".encode()

def hash_state_proof_message(
  message: dict
):
  spm_serialized = serialize_state_proof_message(
    b64decode(message['BlockHeadersCommitment']),
    b64decode(message['VotersCommitment']),
    message['LnProvenWeight'],
    message['FirstAttestedRound'],
    message['LastAttestedRound']
  )

  m = sha256()
  m.update(state_proof_message_prefix + spm_serialized)
  return m.digest()

class StateProofOracle:
  def __new__(
    self,
    first_attested_round: int, # uint64
    interval_size: int, # uint64
    genesis_voters_commitment: bytes, # 32 bytes
    genesis_ln_proven_weight: int, # uint64
    capacity: int, # uint64
  ):
    self.voters_commitment = genesis_voters_commitment
    self.ln_proven_weight = genesis_ln_proven_weight
    self.block_interval_commitment_history = CommitmentHistory(
      first_attested_round,
      interval_size,
      capacity
    )
  
  def advance_state(
    self,
    state_proof: bytes, # bytes
    message: dict # state proof response
  ):
    verifier = StateProofVerifier(
      self.voters_commitment,
      self.ln_proven_weight
    )

    message_hash = hash_state_proof_message(message)

    verifier.verify(
      message['LastAttestedRound'],
      message_hash,
      state_proof
    )

    self.voters_commitment = b64decode(message['VotersCommitment'])
    self.ln_proven_weight = message['LnProvenWeight']

    self.block_interval_commitment_history.insert_commitment(
      b64decode(message['BlockHeadersCommitment'])
    )

class CommitmentHistory:
  def __new__(
    self,
    first_attested_round: int, # uint64
    interval_size: int, # uint64
    capacity: int # uint64
  ):
    self.first_attested_round = first_attested_round
    self.interval_size = interval_size
    self.capacity = capacity
    self.earliest_interval = 0
    self.next_interval = 0
    self.data = {} # map from uint64 -> bytes32

  def insert_commitment(
    commitment: bytes # 32 bytes
  ):
    raise Exception("Not implemented")

class StateProofVerifier:
  def __new__(
    self,
    participants_commitment: bytes, # 32 bytes
    ln_proven_weight: int # uint64
  ):
    self.strength_target = strength_target
    self.ln_proven_weight = ln_proven_weight
    self.participants_commitment = participants_commitment

  def verify(
    round: int, # uint64
    data: bytes, # 32 bytes
    s: bytes
  ):
    raise Exception("Not implemented")