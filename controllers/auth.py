from services.firebase import db

class UserNotFoundError(Exception):
    pass

def auth(req):
    userData = req['data']
    email = userData['email']
    user = db.collection('users').document(email).get()
    res = {}
    if user.exists:
        res = user.to_dict()
        return res
    else:
        raise UserNotFoundError('User not found')