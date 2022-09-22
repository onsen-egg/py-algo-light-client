import pickle
import algosdk

round_num = 24282000
tx_id = "KY7MZK6PPFSFCPR5XOKROLXSDB35QT3XHG7Z477CS4T64H6L4Z3A"

token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
net = "http://localhost:4001"
# token = "842126029"
# net = "https://mainnet-api.algonode.cloud"
client = algosdk.v2client.algod.AlgodClient(token, net)

state_proof = client.stateproofs(round_num)
with open("state_proof", "wb") as f:
  pickle.dump(state_proof, f)

lightblockheader_proof = client.lightblockheader_proof(round_num)
with open("lightblockheader_proof", "wb") as f:
  pickle.dump(lightblockheader_proof, f)

transaction_proof = client.transaction_proof(round_num, tx_id)
with open("transaction_proof", "wb") as f:
  pickle.dump(transaction_proof, f)
