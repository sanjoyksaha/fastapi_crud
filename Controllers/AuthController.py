from datetime import datetime, timedelta
from operator import and_
import hashlib
from sqlalchemy.orm import Session

from Database import models
from Module.jobs import job_crud



def Login(db: Session, request):
    """
    First check user has any pending job
    """
    check_user = db.query(models.User).filter(models.User.unq_id == request.userid).first()
    if not check_user:
        return {"status": 0, "msg": "Invalid UserID. Please try again with a valid UserID."}
    currentTimeStamp = int(datetime.now().timestamp())
    print("user", check_user.id)

    check_token = db.query(models.UserTokens).filter(models.UserTokens.user_id == check_user.id,
                                                          models.UserTokens.status == 1,
                                                          models.UserTokens.expired_at > currentTimeStamp).first()
    token = ""
    if check_token is None:
        # Insert Token
        passw = str(check_user.id) + ":" + str(check_user.unq_id) + ":" + str(currentTimeStamp)
        hashed = hashlib.sha256(passw.encode()).hexdigest()
        token = 'Bearer ' + hashed
        print(currentTimeStamp)
        expired = int((datetime.now() + timedelta(minutes=3000)).timestamp())
        print(expired)

        insertToken = models.UserTokens(user_id=check_user.id, token=token, expired_at=expired, status=1)
        db.add(insertToken)
        db.commit()
        db.refresh(insertToken)
        print(token)
    else:
        token = check_token.token

    return {"status": 1, "msg": "Successfully Logged In!", "token": token}

    # insert = job_crud.InsertJob(db, request)
    # if insert.id > 0:
    #     return {"status": 1, "msg": "Success."}
    # return {"status": 0, "msg": insert}


