import hashlib
import json
import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=1, previous_hash="0000000000000000000") # Genesis block

    def hash(self, block):
        #solution
        # block['transactions'] = json.dumps(block['transactions'], sort_keys=True)
        

        json_from_block = json.dumps(block, sort_keys=True)
        print(json_from_block)
        encoded_block = json_from_block.encode()
        return hashlib.sha256(encoded_block).hexdigest()


    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
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

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]
            
            # if is correctly connected
            if curr_block["previous_hash"] != self.hash(prev_block):
                print("1")
                return False

            # if last proof is valid
            proof_valid = hashlib.sha256(str(curr_block["proof"]**2 - prev_block["proof"]**2).encode()).hexdigest()
            if proof_valid[:4] != "0000":
                print("2")
                return False
            


        return True



# blockchain = Blockchain()

# blockchain.new_transaction('Alice', 'Bob', 1)
# blockchain.new_transaction('Bob', 'Charlie', 2)
# blockchain.new_transaction('Charlie', 'Alice', 3)

# previous_block = blockchain.get_previous_block()
# proof = blockchain.proof_of_work(previous_block['proof'])
# block = blockchain.create_block(proof, blockchain.hash(previous_block))

# # print(blockchain.chain)
# blockchain.chain[1]['transactions'] = []
# # print(blockchain.chain)
# print(blockchain.is_chain_valid())


    



