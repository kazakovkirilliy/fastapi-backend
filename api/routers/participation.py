from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import database, oauth2, models

from ..schemas import participation, token

router = APIRouter(prefix="/participation", tags=["participation"])


@router.post("")
def participation_toggle_one(participation: participation.Participation, db: Session = Depends(database.get_db), token_data: token.TokenData = Depends(oauth2.get_current_user)):

    participation_query = db.query(models.Participation).filter(models.Participation.post_id ==
                                                                participation.post_id, models.Participation.user_id == token_data.user_id)

    participation_fetched = participation_query.first()

    if participation_fetched == None:
        new_participation = models.Participation(
            user_id=token_data.user_id, post_id=participation.post_id)

        db.add(new_participation)
        db.commit()

        # Post added to favorites
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        participation_query.delete(synchronize_session=False)
        db.commit()

        # Post removed from favorites
        return Response(status_code=status.HTTP_204_NO_CONTENT)
