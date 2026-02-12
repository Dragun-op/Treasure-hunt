import hashlib

def hash_answer(answer: str) -> str:
    normalized = answer.strip().lower()
    return hashlib.sha256(normalized.encode()).hexdigest()
