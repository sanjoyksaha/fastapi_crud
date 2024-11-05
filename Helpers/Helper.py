from datetime import datetime
from sqlalchemy.orm import Session

from Database import models


def AuthenticateByToken(request, db:Session):
    if 'authorization' in request.headers:
        token = request.headers['authorization']
        if token != '':
            currentTimeStamp = int(datetime.now().timestamp())
            tokenData = db.query(models.UserTokens).filter(models.UserTokens.token == token,
                                                           models.UserTokens.expired_at > currentTimeStamp,
                                                           models.UserTokens.status == 1).first()
            if tokenData is not None:
                user = db.query(models.User).filter(models.User.id == tokenData.user_id).first()
                return {'id': user.id, 'name': user.name, 'is_superadmin': user.is_superadmin, 'token': tokenData.token, 'status': 1}
            else:
                return []
        else:
            return []
    else:
        return []


