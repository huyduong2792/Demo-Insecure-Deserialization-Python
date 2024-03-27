import pickle, base64
import hashlib
import os
from app.config import settings

class RequiresLoginException(Exception):
    pass
class CurrentUser:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

def make_password_hash(password):
    password_hash = hashlib.sha256((password + settings.salt).encode()).hexdigest()
    return password_hash

def gen_login_session(username, password_hash):
    curr_user = CurrentUser(username, password_hash)
    ser = pickle.dumps(curr_user)
    b64 = base64.b64encode(ser)
    return b64.decode('utf-8')