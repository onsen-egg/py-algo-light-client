import pickle
import base64
import algosdk

round_num = 24284400
tx_id = "MBTWPWSMPISSNIHWZ6OO7QJZCMCLC4H55HVWHZHJB33XJCWKP5BA"
tx_hash = base64.b64encode(base64.b32decode(tx_id + "===="))

# token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
# net = "http://localhost:4001"
token = "842126029"
net = "https://testnet-api.algonode.cloud:4001"
client = algosdk.v2client.algod.AlgodClient(token, net)
print('hey')
state_proof = client.stateproofs(round_num)
# with open("state_proof", "wb") as f:
#   pickle.dump(state_proof, f)

lightblockheader_proof = client.lightblockheader_proof(round_num)
# with open("lightblockheader_proof", "wb") as f:
#   pickle.dump(lightblockheader_proof, f)

transaction_proof = client.transaction_proof(round_num, tx_id, hashtype="sha256")
# with open("transaction_proof", "wb") as f:
#   pickle.dump(transaction_proof, f)

block_info = client.block_info(round_num)
# with open("block_info", "wb") as f:
#   pickle.dump(block_info["block"], f)

# with open("tx_hash_b64", "wb") as f:
#   pickle.dump(tx_hash, f)