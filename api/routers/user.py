"""
Main User API.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import PlainTextResponse, JSONResponse

from api.models import User
from api.routers.common import RequestPager, ResponsePager
from .. import utils

from ..schemas import user

from ..database import get_db


from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["users"])


# @router.get("")
# def user_get_all(paging: RequestPager = Depends(), db: Session = Depends(get_db)):

#     content = db.query(User).offset(paging.offset).limit(paging.limit).all()
#     total_count = db.query(User).count()

#     return ResponsePager(
#         content=content,
#         count=len(content),
#         limit=paging.limit,
#         offset=paging.offset,
#         order=paging.order,
#         order_by=paging.order_by,
#         total_count=total_count,
#     )


@router.get("/{user_id}", response_model=user.UserResponse, response_class=JSONResponse)
def user_get_one(user_id: str, db: Session = Depends(get_db)):
    """
    Read specific user.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} was not found")

    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user.UserResponse)
def user_create_one(user: user.UserCreate, db: Session = Depends(get_db)):

    # hash password
    hashed_password = utils.hash(string=user.password)
    user.password = hashed_password

    new_user = User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{user_id}")
def user_update_one(user_id: str, updated_user: user.UserUpdate, db: Session = Depends(get_db)):
    """
    Update existing user
    """
    user_query = db.query(User).filter(User.id == user_id)

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} does not exist")

    user_query.update(updated_user.dict(exclude_unset=True),
                      synchronize_session=False)

    db.commit()

    return user_query.first()


# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def user_delete_one(user_id: str, db: Session = Depends(get_db)):
#     """
#     Delete user
#     """
#     user_query = db.query(User).filter(User.id == user_id)

#     if user_query.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id: {user_id} was not found")

#     user_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
