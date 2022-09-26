from hashlib import sha256
import algosdk
import os
import sys
from base64 import b32decode, b64decode
from block_fetcher import decode_block
from hashlib import sha256


# In CLI run: python3 generate_proof_assets.py <FOLDER_NAME> <NETWORK>
# <NETWORK> is optional, can be mainnet or testnet

def generate_proof_assets(folder_name, network='testnet'):
  token = ''
  net = 'https://{}-api.algonode.cloud'.format(network)

  client = algosdk.v2client.algod.AlgodClient(token, net)
  idx_net = 'https://{}-idx.algonode.cloud'.format(network)
  indexer = algosdk.v2client.indexer.IndexerClient(token, idx_net)

  client_old = algosdk.algod.AlgodClient(token, net)
  if os.path.exists(folder_name):
    raise Exception('The folder name {} is already in use'.format(folder_name))

  os.mkdir(folder_name)

  # blocks are generated every 256 rounds
  status = client.status()
  round_num = status['last-round'] - 512 

  state_proof = client.stateproofs(round_num)

  block_txns = decode_block(client.block_info(round_num, response_format='msgpack'))
  txn_to_validate = block_txns[0].txn

  txn_bytes = b64decode(algosdk.encoding.msgpack_encode(txn_to_validate.transaction))
  hasher = sha256()
  hasher.update(b'TX' + txn_bytes)
  tx_raw_hash = hasher.digest()

  lightblockheader_proof = client.lightblockheader_proof(round_num)
  transaction_proof = client.transaction_proof(round_num, txn_to_validate.get_txid(), hashtype='sha256')
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
  tx_assets['transaction_id.txt'] = str(list(tx_raw_hash)).replace(' ', '')
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
  if len(sys.argv) > 2:
    generate_proof_assets(sys.argv[1], sys.argv[2])
  else:
    generate_proof_assets(sys.argv[1])
