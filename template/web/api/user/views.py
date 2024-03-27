from fastapi import APIRouter, Depends, HTTPException

from template.web.api.user.schema import UserCreate, UserInDB, UserUpdate
from template.services.user import UserService
from template.security.depends import token_verifier
from typing import List

router = APIRouter(dependencies=[Depends(token_verifier)])


@router.post("/", response_model=UserInDB, status_code=201)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(),
):
        created_user = await user_service.create_user(user=user)
        user_response = UserInDB(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            fullname=created_user.fullname,
            is_superuser=created_user.is_superuser
        )
        return user_response


@router.get("/", response_model=List[UserInDB])
async def get_users(
    user_service: UserService = Depends(),
    limit: int = 10,
    offset: int = 0,
) -> List[UserInDB]:
    try:
        users = await user_service.get_users(limit=limit, offset=offset)
        users_result = [
            UserInDB(
                id=user.id,
                username=user.username,
                email=user.email,
                fullname=user.fullname,
                is_superuser=user.is_superuser,
            )
            for user in users
        ]

        return users_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{id}", response_model=UserInDB)
async def get_user_by_id(
    user_service: UserService = Depends(),
    id: int = None
) -> UserInDB:
            user = await user_service.get_user_by_id(id)
            
            users_result = UserInDB(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    fullname=user.fullname,
                    is_superuser=user.is_superuser,
                )

            return users_result


@router.patch("/{id}", response_model=UserInDB)
async def update_user(
    user : UserUpdate,
    user_service: UserService = Depends(),
    id: int = None
) -> UserInDB:
    
    user_updated = await user_service.update_user(id, user)
    
    users_result = UserInDB(
            id=user_updated.id,
            username=user_updated.username,
            email=user_updated.email,
            fullname=user_updated.fullname,
            is_superuser=user_updated.is_superuser,
        )

    return users_result


@router.delete("/{id}", response_model=UserInDB)
async def delete_user(
    user_service: UserService = Depends(),
    id: int = None
) -> UserInDB:

    deleted_user = await user_service.delete_user(id)
    users_result = UserInDB(
            id=deleted_user.id,
            username=deleted_user.username,
            email=deleted_user.email,
            fullname=deleted_user.fullname,
            is_superuser=deleted_user.is_superuser,
        )

    return users_result
        
