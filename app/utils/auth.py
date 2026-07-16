from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError
from fastapi import HTTPException

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5   # Token valid for 5 minutes

def create_access_token(user_key: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"user_key": user_key, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_key")
    except ExpiredSignatureError:
        # Token expired → return proper 401 error
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        # Invalid token → return proper 401 error
        raise HTTPException(status_code=401, detail="Invalid token")



#from datetime import datetime, timedelta
#from jose import jwt

#SECRET_KEY = "your-secret-key"
#ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 30

#def create_access_token(user_key: str):
 #   expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
 #   to_encode = {"user_key": user_key, "exp": expire}
#    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#    return encoded_jwt

#def decode_token(token: str):
#    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#    user_key = payload.get("user_key")
 #   return user_key
