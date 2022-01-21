"""
Providing encryption functions for password functionality.
"""
from hashlib import *


def encrypt(password: str):
    """
    Convert a string into an md5 encrypted string.
    :param password: String to convert
    :return: Converted md5 string
    """
    return md5(password.encode()).hexdigest()
