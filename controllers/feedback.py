from services.firebase import db

def getFeedback():
    feedbacks = db.collection('feedback').get()
    res = []
    for feedback in feedbacks:
        res.append({ 'id': feedback.id, **feedback.to_dict() })
    return res


def feedback(data):
    action = data['action']
    if (action == 'get'):
        return getFeedback()
    if (action == 'add'):
        feedbackData = data['data']
        db.collection('feedback').add(feedbackData)
        return 'Feedback added successfully!'
    if (action == 'delete'):
        feedbackId = data['id']
        db.collection('feedback').document(feedbackId).delete()
        return 'Feedback deleted successfully!'
    return 'Invalid action!'