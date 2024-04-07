import pickle, base64
import hashlib
import os
from app.config import settings

class RequiresLoginException(Exception):
    pass
class CurrentUser:
    def __init__(self, user_id, username, password_hash):
        self.user_id = str(user_id)
        self.username = username
        self.password_hash = password_hash

def make_password_hash(password):
    password_hash = hashlib.sha256((password + settings.salt).encode()).hexdigest()
    return password_hash

def gen_login_session(user_id, username, password_hash):
    print("===user_id===", user_id)
    curr_user = CurrentUser(user_id, username, password_hash)
    ser = pickle.dumps(curr_user)
    b64 = base64.b64encode(ser)
    return b64.decode('utf-8')