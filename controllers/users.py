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
    return 'Invalid action!'
    