from database.models import Usage
from database.db import db_session

def track_usage(user_id):
    usage = Usage(user_id=user_id)
    db_session.add(usage)
    db_session.commit()
    return {"status": "success", "message": "Usage tracked"}
