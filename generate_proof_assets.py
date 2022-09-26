import algosdk
import os
import sys
from base64 import b32decode, b64decode

# In CLI run: python3 generate_proof_assets.py [FOLDER_NAME]

def generate_proof_assets(folder_name):
  token = ""
  net = "https://testnet-api.algonode.cloud"

  client = algosdk.v2client.algod.AlgodClient(token, net)
  idx_net = "https://testnet-idx.algonode.cloud"
  indexer = algosdk.v2client.indexer.IndexerClient(token, idx_net)

  if os.path.exists(folder_name):
    raise Exception('The folder name {} is already in use'.format(folder_name))

  os.mkdir(folder_name)

  # blocks are generated every 256 rounds
  status = client.status()
  round_num = status['last-round'] - 512 

  txns_for_round = indexer.search_transactions(limit=10, round_num=round_num)

  tx_id = txns_for_round['transactions'][0]['id']

  state_proof = client.stateproofs(round_num) 
  first_round = state_proof['Message']['FirstAttestedRound']

  lightblockheader_proof = client.lightblockheader_proof(round_num)
  transaction_proof = client.transaction_proof(round_num, tx_id, hashtype='sha256')
  block_info = client.block_info(round_num)
  prev_block_info = client.block_info(round_num - 1)

  genesis_assets = {}

  state_proof_assets = {}
  state_proof_assets['state_proof_message.json'] = str(state_proof['Message']).replace('\'', '\"').replace(' ', '')
  state_proof_assets['state_proof.txt'] = '\"' + state_proof['StateProof'] + '\"'

  tx_assets = {}
  tx_assets['genesis_hash.txt'] = str(list(b64decode(block_info['block']['gh']))).replace(' ', '')
  tx_assets['light_block_header_proof_response.json'] = str(lightblockheader_proof).replace('\'', '\"').replace(' ', '')
  tx_assets['round.txt'] = str(round_num)
  tx_assets['seed.txt'] = str(list(b64decode(block_info['block']['seed']))).replace(' ', '')
  tx_assets['transaction_id.txt'] = str(list(b32decode(tx_id + '===='))).replace(' ', '')
  tx_assets['transaction_proof_response.json'] = str(transaction_proof).replace('\'', '\"').replace(' ', '')

  for pair in zip(
    [genesis_assets, state_proof_assets, tx_assets],
    ['genesis', 'stateproofverification', 'transactionverification']
  ):
    os.mkdir(os.path.join(folder_name, pair[1]))
    for k in pair[0].keys():
      with open(os.path.join(
        folder_name, 
        pair[1],
        k), 'w') as f:
        f.write(str(pair[0][k]))


if __name__ == '__main__':
  generate_proof_assets(sys.argv[1])
  