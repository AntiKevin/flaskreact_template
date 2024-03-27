import os
import time
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
from template.services.user import UserService

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

SECRET_KEY = os.environ.get("TEMPLATE_JWT_SECRET")
ALGORITHM = os.environ.get("TEMPLATE_JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 2 # 2 horas
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 4 # 4 horas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JWTSecurity:
    
    def create_jwt_token(self, data: dict):
        to_encode_token = data.copy()
        expire = int(time.time()) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        to_encode_token.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode_token, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_refresh_jwt_token(self, data: dict):
        to_encode_refresh_token = data.copy()
        refresh_expire = int(time.time()) + (REFRESH_TOKEN_EXPIRE_MINUTES * 60)
        to_encode_refresh_token.update({"exp": refresh_expire})
        encoded_refresh_jwt = jwt.encode(to_encode_refresh_token, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_refresh_jwt


    def decode_jwt_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
            status_code=401,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async def verify_token(self, user_service: UserService, access_token):

        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail='Token invalido'
            )
        
        user_on_db = await user_service.get_user_by_username(username=data['username'])

        data_atual_timestamp = int(time.time())
        
        if (data['exp']<= data_atual_timestamp):
            raise HTTPException(
                status_code=401,
                detail='Token Expirado'
            )

        if user_on_db is None:
            raise HTTPException(
                status_code=401,
                detail='Token invalido'
            )
    

    async def refresh_token(self, refresh_token):

        try:
            data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError: raise HTTPException(
                status_code=401,
                detail='Token invalido'
            )
            
        data_atual_timestamp = int(time.time())

        if ((data['exp'] > data_atual_timestamp)): # caso não tenha expirado
                new_token = self.create_jwt_token({'username':data['username']})
                new_refresh_token = self.create_refresh_jwt_token({'username':data['username']})

        else: raise HTTPException(
                status_code=401,
                detail='Token expirado'
            )
        
        
        return {"access_token": new_token, "refresh_token": new_refresh_token}

        