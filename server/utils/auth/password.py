from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Create a hashed password.

    Args:
        password (str): password to be hashed

    Returns:
        str: hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password from hashed one.

    Args:
        plain_password (str): plain password
        hashed_password (str): hashed password

    Returns:
        bool: the matching condition of two given passwords
    """
    return pwd_context.verify(plain_password, hashed_password)
