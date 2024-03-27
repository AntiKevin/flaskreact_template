from fastapi import APIRouter, Depends, HTTPException

from template.security.auth import JWTSecurity
from template.security.depends import token_verifier
from template.services.user import UserService
from template.web.api.auth.schema import AuthLogin, AuthToken
from template.web.api.user.schema import UserInDB

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    user_login: AuthLogin,
    jwt_security: JWTSecurity = Depends(),
    user_service: UserService = Depends()
    ) -> dict:
    user_in_db = await user_service.get_user_by_username(user_login.username)
    if (user_in_db != None and user_in_db.password == user_login.password):
        token = jwt_security.create_jwt_token({'username':user_login.username})
        refresh_token = jwt_security.create_refresh_jwt_token({'username':user_login.username})
        return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail=f"O Usuário ou senha incorretos")

@router.post("/refresh-token")
async def refresh_token(
    user_token: AuthToken,
    jwt_security: JWTSecurity = Depends()
    ) -> dict:

    refreshed_tokens = await jwt_security.refresh_token(refresh_token=user_token.refresh_token)
    return {"access_token": refreshed_tokens['access_token'], "refresh_token": refreshed_tokens['refresh_token'], "token_type": "bearer"}

@router.get("/logged-user")
async def logged_user(logged_user = Depends(token_verifier)) -> UserInDB:
    return logged_user
