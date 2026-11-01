import hashlib
import secrets


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        200000
    ).hex()

    return f"pbkdf2_sha256${salt}${password_hash}"


def verify_password(password, stored_password):
    if stored_password.startswith("pbkdf2_sha256$"):
        try:
            _, salt, saved_hash = stored_password.split("$")

            new_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode(),
                salt.encode(),
                200000
            ).hex()

            return secrets.compare_digest(new_hash, saved_hash)
        except ValueError:
            return False

    # Supports the existing sample accounts temporarily.
    return secrets.compare_digest(password, stored_password)