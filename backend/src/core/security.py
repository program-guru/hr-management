from pwdlib import PasswordHash

# Create a PasswordHash instance using the recommended settings for Argon2.
password_hash = PasswordHash.recommended()

# Verifies a plain password against a hashed password.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

# Hashes a plain password and returns the hashed version.
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)