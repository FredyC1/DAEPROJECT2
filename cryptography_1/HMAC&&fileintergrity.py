import hmac
import hashlib

def generate_hmac(key: bytes, message: bytes) -> bytes:
    """Generates an HMAC for the given message using SHA-256."""
    return hmac.new(key, message, hashlib.sha256).digest()

def verify_hmac(key: bytes, message: bytes, expected_hmac: bytes) -> bool:
    """Verifies if the provided HMAC matches the expected HMAC."""
    return hmac.compare_digest(generate_hmac(key, message), expected_hmac)

def compute_file_hmac(key: bytes, file_path: str) -> bytes:
    """Computes the HMAC of a file's contents."""
    h = hmac.new(key, digestmod=hashlib.sha256)
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.digest()

def verify_file_integrity(key: bytes, file_path: str, expected_hmac: bytes) -> bool:
    """Verifies the integrity of a file by comparing its computed HMAC with the expected one."""
    return hmac.compare_digest(compute_file_hmac(key, file_path), expected_hmac)

# Example usage
if __name__ == "__main__":
    secret_key = b'supersecretkey'
    message = b'Important message'
    file_path = 'example.txt'
    
    # Generate and verify message HMAC
    message_hmac = generate_hmac(secret_key, message)
    print("Message HMAC Verified:", verify_hmac(secret_key, message, message_hmac))
    
    # Compute and verify file integrity
    file_hmac = compute_file_hmac(secret_key, file_path)
    print("File Integrity Verified:", verify_file_integrity(secret_key, file_path, file_hmac))
