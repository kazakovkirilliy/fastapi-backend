from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import database, oauth2, models

from ..schemas import like, token

router = APIRouter(prefix="/like", tags=["like"])


@router.post("")
def like_toggle_one(like: like.Like, db: Session = Depends(database.get_db), token_data: token.TokenData = Depends(oauth2.get_current_user)):

    like_query = db.query(models.Like).filter(models.Like.post_id ==
                                              like.post_id, models.Like.user_id == token_data.user_id)

    like_fetched = like_query.first()

    if like_fetched == None:
        new_like = models.Like(
            user_id=token_data.user_id, post_id=like.post_id)

        db.add(new_like)
        db.commit()

        # Post added to favorites
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        like_query.delete(synchronize_session=False)
        db.commit()

        # Post removed from favorites
        return Response(status_code=status.HTTP_204_NO_CONTENT)
