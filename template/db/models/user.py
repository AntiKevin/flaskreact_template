from template.db.base import Base
from typing import Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import PasswordType, EmailType


class User(Base):
    """Model for demo purpose."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[Optional[str]] = mapped_column(String(30))
    is_superuser: Mapped[bool] = mapped_column(Boolean())
    email: Mapped[Optional[str]] = mapped_column(EmailType(), unique=True)
    password: Mapped[str] = mapped_column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))
