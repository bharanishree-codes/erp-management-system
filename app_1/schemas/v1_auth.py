from pydantic import BaseModel

class UserKeyInput(BaseModel):
    user_key: str
    secrete_key: str
    user_type: str
    user_url: str

class SecretKeyInput(BaseModel):
    secret_key: str