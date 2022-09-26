import algosdk
import os
from base64 import b32decode, b64decode

folder_name = 'test_assets_3'

round_num = 24377196
tx_id = 'BJLYHXER7HHG3RMIX3VQNQM2YIRRIVPOEAILOXU2TK6J4R7RI44Q'

token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
net = 'http://localhost:4001'
# token = "842126029"
# net = "https://testnet-api.algonode.cloud:4001"

client = algosdk.v2client.algod.AlgodClient(token, net)

if os.path.exists(folder_name):
  raise Exception('The folder name {} is already in use'.format(folder_name))

os.mkdir(folder_name)

# genesis = client.genesis()
state_proof = client.stateproofs(round_num)
lightblockheader_proof = client.lightblockheader_proof(round_num)
transaction_proof = client.transaction_proof(round_num, tx_id, hashtype='sha256')
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

