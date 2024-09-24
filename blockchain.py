from block import Block
from pysondb import getDb
from hashlib import sha256
import concurrent.futures
from multiprocessing import cpu_count

class Blockchain:
    
    def __init__(self):
        self.pending_blocks = []
        self.proof_zeros_count = 3
        self.blocks_list = getDb('blockchain.json')
        saved_blocks = self.blocks_list.getAll()

        if len(saved_blocks) > 0:
            self.chain = []
            for block in saved_blocks:
                new_block = Block()
                new_block.read(block['proof'], block['previous_hash'], block['data'], block['timestamp'], block['hash'])
                self.chain.append(new_block)
        else:
            self.chain = [Block().create(1, '0', {
                'data': "Genesis Block"
            })]
            self.blocks_list.add({
                'previous_hash': self.chain[0].previous_hash,
                'hash': self.chain[0].hash,
                'timestamp': self.chain[0].timestamp,
                'data': self.chain[0].data,
                'proof': self.chain[0].proof
            })

    def get_proof(self):
        new_proof = 0
        hashes = ""
        for blocks in self.chain:
            hashes += blocks.hash
        while not self.found_proof:
            hash_operation = sha256((str(new_proof) + hashes).encode()).hexdigest()
            if hash_operation.startswith('0' * self.proof_zeros_count):
                self.found_proof = True
                return new_proof
            new_proof += 1
        return 0
    
    def add_block(self, data):
        previous_hash = self.chain[-1].hash
        self.found_proof = False

        with concurrent.futures.ThreadPoolExecutor() as executor:
            processes = [executor.submit(self.get_proof) for _ in range(cpu_count() - 1)]
            for process in concurrent.futures.as_completed(processes):
                self.pending_blocks.append({'data': data, 'previous_hash': previous_hash})
                if process.result() == 0:
                    continue
                block = Block().create(process.result(), previous_hash, data)

        self.chain.append(block)
        self.blocks_list.add({
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'timestamp': block.timestamp,
            'data': block.data,
            'proof': block.proof
        })
        self.pending_blocks.pop()
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            hashes = ""
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            for blocks in self.chain[:i]:
                hashes += blocks.hash

            if sha256((str(current_block.proof) + hashes).encode()).hexdigest().startswith('0' * self.proof_zeros_count) != True:
                return False
            elif current_block.hash != current_block.calculate_hash():
                return False
            elif current_block.previous_hash != previous_block.hash:
                return False

        return True