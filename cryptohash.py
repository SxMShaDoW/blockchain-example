import struct
import json
import hashlib

def cryptohash(msg, number, diffculty):
    """ Create a sha256 hash for a given block at a given difficulty """
    leading_bytes = '0'
    block_hash = hashlib.sha256()
    # Compute hash for the ’block’ first
    block_hash.update(json.dumps(msg).encode()) 
    for nonce in range(0, number):
        # Convert out ‘number’ to binary encoding
        nonce_bin = struct.pack("<I", nonce)
        block_hash_copy = block_hash.copy() 
        # Compute cryptohash(msg, number)
        block_hash_copy.update(nonce_bin)
        hash_hex = block_hash_copy.hexdigest()
        # Check if leading 16 bytes are zero 
        if hash_hex[:diffculty] != leading_bytes * diffculty:
            continue
        return (nonce, hash_hex)
    # make the code easier if can't create a hash
    cryptohash(msg, number, diffculty - 1)