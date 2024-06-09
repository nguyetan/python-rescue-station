from services.firebase import db

def auth(req):
    userData = req['data']
    email = userData['email']
    user = db.collection('users').document(email).get()
    res = {}
    if (user.exists):
        res = user.to_dict()
    else:
        db.collection('users').document(email).set(userData)
        res = userData
    return res