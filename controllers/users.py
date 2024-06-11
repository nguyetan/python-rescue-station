from services.firebase import db

def getUsers():
    users = db.collection('users').get()
    res = []
    for user in users:
        res.append(user.to_dict())
    return res

def usersController(req):
    action = req['action']
    if (action == 'get'):
        return getUsers()
    if (action == 'add'):
        data = req['data']
        id = data['email']
        db.collection('users').document(id).set(data)
    if (action == 'update'):
        data = req['data']
        id = data['email']
        db.collection('users').document(id).update(data)
    if (action == 'delete'):
        data = req['data']
        id = data['email']
        db.collection('users').document(id).delete()
    return 'Invalid action!'
    