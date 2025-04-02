import hashlib
import json
import time
import os

def load_json():
    if os.path.exists("blockchain.json"):
        with open("blockchain.json", "r", encoding = "utf-8") as f:
            try:
                return json.load(f)
            except: 
                return None
    else:
        return None
    
def save_json(data):
    with open("blockchain.json", "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 2)



class Blockchain:
    def __init__(self):
        chain = load_json()
        if not chain:
            self.chain = []
            self.current_transactions = []
            self.create_block(proof=1, previous_hash="0000000000000000000") # Genesis block
        else:
            self.chain = chain



    def hash(self, block):
        block_copy = json.loads(json.dumps(block))
        
        if "hash" in block_copy:
            del block_copy["hash"]

        json_from_block = json.dumps(block_copy, sort_keys=True)
        encoded_block = json_from_block.encode()
        return hashlib.sha256(encoded_block).hexdigest()


    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        block['hash'] = self.hash(block)
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.get_previous_block()['index'] + 1
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                return new_proof
            new_proof += 1
        save_json(self.chain)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]

            if curr_block["previous_hash"] != prev_block["hash"]:
                print(f"Invalid previous_hash at block {curr_block['index']}")
                return False

            if curr_block["hash"] != self.hash(curr_block):
                print(f"Block {curr_block['index']} has been tampered with")
                return False

            proof_valid = hashlib.sha256(str(curr_block["proof"]**2 - prev_block["proof"]**2).encode()).hexdigest()
            if proof_valid[:4] != "0000":
                print(f"Invalid proof at block {curr_block['index']}")
                return False
            
        return True



# blockchain = Blockchain()
#
# blockchain.new_transaction('Alice', 'Bob', 1)
# blockchain.new_transaction('Bob', 'Charlie', 2)
# blockchain.new_transaction('Charlie', 'Alice', 3)
#
# previous_block = blockchain.get_previous_block()
# proof = blockchain.proof_of_work(previous_block['proof'])
# block = blockchain.create_block(proof, blockchain.hash(previous_block))
#
# print(blockchain.is_chain_valid())


    



