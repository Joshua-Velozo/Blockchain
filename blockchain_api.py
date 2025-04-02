from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain import Blockchain

app = Flask(__name__)
node_id = str(uuid4())
print(node_id)
blockchain = Blockchain()

@app.route("/mine")
def mine():
    last_block = blockchain.get_previous_block()
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(
        sender = "0",
        recipient = node_id,
        amount = 1
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "new block forged",
        "index" : block["index"],
        "transactions" : block["transactions"],
        "proof" : block["proof"],
        "previous_hash" : block["previous_hash"],
        "hash" : blockchain.hash(block)
    }
    return jsonify(response)



@app.route('/transaction', methods = ['POST'])
def add_transaction():
    data = request.get_json()
    blockchain.new_transaction(data['sender'], data['recipient'], data['amount'])
    return "okay"

@app.route('/chain')
def get_chain():
    blocks = blockchain.chain
    return jsonify(blocks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)