import redis.asyncio as redis
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.conf.config import settings


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first() 


async def create_user(body: UserModel, db: Session) -> User:
    new_user = User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_password(user: User, password: str, db: Session) -> None:
    user.password = password
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
