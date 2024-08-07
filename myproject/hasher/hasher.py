import datetime
import hashlib
import random
from uuid import uuid4


class Hasher:
    @staticmethod
    def hash(string: str = None):
        """
        Takes a string and returns a hash string.
        If no string is provided, a new UUID is used to ensure uniqueness.
        """
        if string is None:
            string = str(uuid4())

        salt = str(datetime.datetime.now().timestamp()) + str(random.random())
        pre_hash = f'{salt}-{string}'
        result = hashlib.md5(pre_hash.encode()).hexdigest()
        return result
