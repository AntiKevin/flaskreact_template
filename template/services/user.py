from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from template.db.models.user import User
from template.web.api.user.schema import UserCreate, UserUpdate
from typing import List

from template.db.dependencies import get_db_session


class UserService:

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(self, user: UserCreate) -> User:
        """
        checa se usuário já existe no banco, caso não, cria um novo
        """
        db: AsyncSession = self.session

        is_username_in_db = await self.get_user_by_username(username=user.username)
        is_email_in_db = await self.get_user_by_email(email=user.email)

        if (is_email_in_db != None):
            raise HTTPException(status_code=409, detail=f"Email indisponível")
        if (is_username_in_db != None):
            raise HTTPException(status_code=409, detail=f"Usuário indisponível")

        try:
            db_user = User(
                username=user.username,
                email=user.email,
                fullname=user.fullname,
                password=user.password,
                is_superuser=user.is_superuser
            )

            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)

            return db_user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await db.close()
                
        
        

    async def get_user_by_username(self, username: str) -> User:
        db: AsyncSession = self.session
        if (username == None):
            raise HTTPException(status_code=409, detail=f"Username inválido")
        try:
            result = await db.execute(select(User).filter(User.username == username))
            if(result == None):
                raise HTTPException(status_code=404, detail="Usuário com o username informado, Não foi encontrado")
            
            return result.scalar_one_or_none()
        finally:
            await db.close()
    
    async def get_user_by_email(self, email: str) -> User:
        db: AsyncSession = self.session
        if (email == None):
            raise HTTPException(status_code=409, detail=f"Email inválido")
        try:
            result = await db.execute(select(User).filter(User.email == email))
            if(result == None):
                raise HTTPException(status_code=404, detail="Usuário com o email informado, Não foi encontrado")
            
            return result.scalar_one_or_none()
        finally:
            await db.close()

    async def get_user_by_id(self, id: int) -> User:
        db: AsyncSession = self.session
        if (id == None):
            raise HTTPException(status_code=409, detail=f"id inválido")
        try:
            result = await db.execute(select(User).filter(User.id == id))
            if(result == None):
                raise HTTPException(status_code=404, detail="Usuário com o id informado, Não foi encontrado")
            
            return result.scalar_one_or_none()
        finally:
            await db.close()

    async def get_users(self, limit: int, offset: int) -> List[User]:
        db: AsyncSession = self.session
        try:
            result = await db.execute(select(User).limit(limit).offset(offset))
            users = result.scalars().all()
            return users
        finally:
            await db.close()


    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        db: AsyncSession = self.session
        if (user_id == None):
            raise HTTPException(status_code=400, detail="Parâmetro id ausente na solicitação.")
        try:
            db_user = await db.get(User, user_id)
            if (db_user == None):
                raise HTTPException(status_code=404, detail="Usuário com o id informado, Não foi encontrado")
            
            user_update_dict = user_update.model_dump(exclude_unset=True)

            for field, value in user_update_dict.items():
                setattr(db_user, field, value)

            await db.commit()
            await db.refresh(db_user)
            return db_user
            
        finally:
            await db.close()


    async def delete_user(self, user_id: int) -> User:
        db: AsyncSession = self.session
        if (user_id == None):
            raise HTTPException(status_code=400, detail="Parâmetro (id) ausente na solicitação.")  
        
        try:
            db_user = await db.get(User, user_id)
            if (db_user == None):
                raise HTTPException(status_code=404, detail="Usuário com o id informado, Não foi encontrado")
            
            await db.delete(db_user)
            await db.commit()
            return db_user
        
        finally:
            await db.close()
