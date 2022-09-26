from hashlib import sha256
import algosdk
import os
from base64 import b32decode, b64decode, decode
from block_fetcher import decode_block

folder_name = 'test_assets_4'

round_num = 24378520 
tx_id = 'BJLYHXER7HHG3RMIX3VQNQM2YIRRIVPOEAILOXU2TK6J4R7RI44Q'

#token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
#net = 'http://localhost:4001'

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


state_proof = client.stateproofs(round_num) 
first_round = state_proof['Message']['FirstAttestedRound']

block_txns = decode_block(client.block_info(round_num, response_format='msgpack'))
txn_to_validate = block_txns[0].txn

txn_bytes = b64decode(algosdk.encoding.msgpack_encode(txn_to_validate.transaction))
hasher = sha256()
hasher.update(txn_bytes)
tx_raw_hash = hasher.digest()

lightblockheader_proof = client.lightblockheader_proof(round_num)
transaction_proof = client.transaction_proof(round_num, txn_to_validate.get_txid(), hashtype='sha256')
block_info = client.block_info(round_num)


genesis_assets = {}

state_proof_assets = {}
state_proof_assets['state_proof_message.json'] = str(state_proof['Message']).replace('\'', '\"').replace(' ', '')
state_proof_assets['state_proof.txt'] = '\"' + state_proof['StateProof'] + '\"'

tx_assets = {}
tx_assets['genesis_hash.txt'] = str(list(b64decode(block_info['block']['gh']))).replace(' ', '')
tx_assets['light_block_header_proof_response.json'] = str(lightblockheader_proof).replace('\'', '\"').replace(' ', '')
tx_assets['round.txt'] = str(round_num)
tx_assets['seed.txt'] = str(list(b64decode(block_info['block']['seed']))).replace(' ', '')
tx_assets['transaction_proof_response.json'] = str(transaction_proof).replace('\'', '\"').replace(' ', '')
tx_assets['transaction_id.txt'] = str(list(tx_raw_hash)).replace(' ', '')


for pair in zip(
  [genesis_assets, state_proof_assets, tx_assets],
  ['genesis', 'stateproofverification', 'transactionverification']
):
  os.mkdir(os.path.join(folder_name, pair[1]))
  for k in pair[0].keys():
    with open(os.path.join( folder_name, pair[1], k), 'w') as f: 
      f.write(str(pair[0][k]))

