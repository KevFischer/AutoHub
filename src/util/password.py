"""
Providing encryption functions for password functionality.
"""
from hashlib import *
import re


capitals = ""


def encrypt(password: str):
    """
    Convert a string into an md5 encrypted string.
    :param password: String to convert
    :return: Converted md5 string
    """
    return md5(password.encode()).hexdigest()


def check_password(password: str):
    """
    Check if the password matches the password properties.
    :param password: Password to check
    :return: True if matching, false if not
    """
    if len(password) < 8:
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[;%&!?#_@$-]", password):
        return False
    elif re.search("\s", password):
        return False
    else:
        return True
