import pickle
import base64

cookie_session = "gASVvAAAAAAAAACMCWFwcC51bHRpc5SMC0N1cnJlbnRVc2VylJOUKYGUfZQojAd1c2VyX2lklIwkMTRlMWI0Y2MtZTEyNy00MDVlLWJhNjItMmYxZjNiYmUzM2NjlIwIdXNlcm5hbWWUjAVodXlkcZSMDXBhc3N3b3JkX2hhc2iUjEBlNGQyZjk0OWE0MDFjMDRlOWNkMGJkNDEwZTMxZDZmODFiNDEzOTc0MTUxZmM0NThjMThkMmQxODZjMzc5MjE5lHViLg=="
unpickled_object = pickle.loads(base64.b64decode(cookie_session))
print(unpickled_object)
print(vars(unpickled_object))