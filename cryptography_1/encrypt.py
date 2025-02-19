# Hash Function 
def custom_hash(data: bytes) -> int:
    hash_val = 0
    prime = 31 
    modulus = 2**32 

    for byte in data:
        hash_val = (hash_val * prime + byte) % modulus  
    
    return hash_val

print(custom_hash(b"DAE is awesome"))



# Asymmetric Key

