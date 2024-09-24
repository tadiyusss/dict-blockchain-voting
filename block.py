import datetime
from hashlib import sha256
class Block:
    
    def create(self, proof, previous_hash, data):
        self.proof = proof
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = str(datetime.datetime.now())
        self.hash = self.calculate_hash()
        return self

    def read(self, proof, previous_hash, data, timestamp, hash):
        self.proof = proof
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.hash = hash

    def calculate_hash(self):
        return sha256((str(self.proof) + str(self.previous_hash) + str(self.data) + str(self.timestamp)).encode()).hexdigest()
    