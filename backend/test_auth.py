from backend.auth import hash_password, verify_password


password = "hello123"

password_hash = hash_password(password)

print("Original password:", password)
print("Hashed password:", password_hash)

print("Correct password:", verify_password("hello123", password_hash))
print("Wrong password:", verify_password("wrong123", password_hash))