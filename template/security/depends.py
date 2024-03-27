from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from template.security.auth import JWTSecurity
from template.services.user import UserService
from template.web.api.user.schema import UserInDB

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def token_verifier(token = Depends(oauth_scheme), user_service = Depends(UserService), jwt_security = Depends(JWTSecurity)) -> UserInDB:
    await jwt_security.verify_token(access_token=token, user_service=user_service)
    user_decoded = jwt_security.decode_jwt_token(token)
    user = await user_service.get_user_by_username(user_decoded['username'])
    user_response = UserInDB(
                id=user.id,
                username=user.username,
                email=user.email,
                fullname=user.fullname,
                is_superuser=user.is_superuser
            )
    return user_response