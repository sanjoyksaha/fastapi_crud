from datetime import datetime, timedelta
from operator import and_
import hashlib
from sqlalchemy.orm import Session

from Database import models
from Helpers import Helper
from Module.dashboard import dashboard_data


def Dashboard(request, db: Session):
    auth = Helper.AuthenticateByToken(request, db)
    print(auth)
    if len(auth) == 0:
        return {"status": 0, "msg": "Unauthorized"}

    if auth['is_superadmin'] == 1:
        data = dashboard_data.AdminDashboardData(db=db)
    else:
        data = dashboard_data.UserDashboardData(db=db, user_id=auth['id'])

    return {"status": 1, "msg": "Successfully Logged In!", "data": data}
