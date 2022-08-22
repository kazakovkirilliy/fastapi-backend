"""
Main Post API.
"""
import ssl
import certifi
import geopy.geocoders
from api.models import Post, PostLocation
from api.oauth2 import get_current_user
from api.routers.common import RequestPager, ResponsePager
from fastapi import APIRouter, Depends, HTTPException, Response, status
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import post, token

ctx = ssl._create_unverified_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

router = APIRouter(prefix="/posts", tags=["posts"])
geolocator = Nominatim(scheme="http", user_agent="124mclas")


@router.get("")
def post_get_all(paging: RequestPager = Depends(), db: Session = Depends(get_db), token_data: token.TokenData = Depends(get_current_user)):

    content = db.query(Post).filter(Post.title.ilike(f"%{paging.search}%")).limit(
        paging.limit).offset(paging.offset).all()
    total_count = db.query(Post).count()

    return ResponsePager[post.PostWithOwner](
        content=content,
        count=len(content),
        limit=paging.limit,
        offset=paging.offset,
        order=paging.order,
        order_by=paging.order_by,
        total_count=total_count,
        search=paging.search
    )


@router.get("/created")
def post_get_all_created(paging: RequestPager = Depends(), db: Session = Depends(get_db), token_data: token.TokenData = Depends(get_current_user)):

    content = db.query(Post).filter(Post.owner_id == token_data.user_id).filter(Post.title.ilike(f"%{paging.search}%")).limit(paging.limit).offset(
        paging.offset).all()

    total_count = db.query(Post).filter(
        Post.owner_id == token_data.user_id).count()

    return ResponsePager(
        content=content,
        count=len(content),
        limit=paging.limit,
        offset=paging.offset,
        order=paging.order,
        order_by=paging.order_by,
        total_count=total_count,
        search=paging.search
    )


@router.get("/{post_id}", response_model=post.PostWithOwner)
def post_get_one(post_id: str, db: Session = Depends(get_db), token_data: token.TokenData = Depends(get_current_user)):
    """
    Read specific post.
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} was not found")

    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=post.PostWithOwner)
def post_create_one(post: post.PostCreate, db: Session = Depends(get_db), token_data: token.TokenData = Depends(get_current_user)):

    post_to_create = {**dict(post)}
    post_to_create.pop("longitude", None)
    post_to_create.pop("latitude", None)

    new_post = Post(owner_id=token_data.user_id, **dict(post_to_create))

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    address = {}

    try:
        addr = geolocator.reverse(
            f"{post.latitude}, {post.longitude}", language='en').raw['address']

        address["country"] = addr["country"]
        address["city"] = addr["city"]
        address["street"] = addr["road"]
        address["house_number"] = addr["house_number"]
    except:
        pass

    new_location = PostLocation(post_id=new_post.id, longitude=post.longitude,
                                latitude=post.latitude, geography=f'SRID=4326;POINT({post.longitude} {post.latitude})', **address)

    db.add(new_location)
    db.commit()

    return new_post


@router.put("/{post_id}", response_model=post.PostWithOwner)
def post_update_one(post_id: str, updated_post: post.PostUpdate, db: Session = Depends(get_db), token_data: token.TokenData = Depends(get_current_user)):
    """
    Update existing post
    """
    post_query = db.query(Post).filter(Post.id == post_id)

    post: Post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} does not exist")

    if post.owner_id != token_data.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(exclude_unset=True),
                      synchronize_session=False)

    db.commit()

    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def post_delete_one(post_id: str, db: Session = Depends(get_db), token_data: token.TokenData = Depends(get_current_user)):
    """
    Delete post
    """
    post_query = db.query(Post).filter(Post.id == post_id)

    post: Post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} was not found")

    print(post.owner_id)
    print(token_data.user_id)

    if str(post.owner_id) != token_data.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
