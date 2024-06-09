from firebase_admin import firestore

db = firestore.client()

def auth(req):
    userData = req['data']
    email = userData['email']
    user = db.collection('users').document(email).get()
    res = {}
    if (user.exists):
        res = { 'data': user.to_dict()}
    else:
        db.collection('users').document(email).set(userData)
        res = { 'data': req }
    return res