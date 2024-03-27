from pydantic import BaseModel


class AuthLogin(BaseModel):
    username: str
    password: str

class AuthToken(BaseModel):
    refresh_token: str
