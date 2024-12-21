from passlib.hash import bcrypt


def check_password(hashed_password, password) -> bool:
    return bcrypt.verify(password, hashed_password)
