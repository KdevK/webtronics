from fastapi import FastAPI, Depends, HTTPException

from auth.services import get_password_hash, check_user, check_email
from data.models import UserLoginSchema, UserCreateSchema, PostCreateSchema, PostResponseSchema, RatePostSchema
from data.methods import create_user, create_post, get_user, delete_post, get_post, update_post, send_rate, delete_rate

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import sign_jwt, decode_jwt

app = FastAPI()


@app.get("/", dependencies=[Depends(JWTBearer())])
async def read_root():
    return {"info": "auth works"}


@app.post("/signup", tags=["Auth"])
async def signup(user: UserCreateSchema):
    if check_email(user.email):
        if user.password == user.password_repeat:
            temp_password = await get_password_hash(user.password)
            if create_user(user.email, temp_password):
                return sign_jwt(user.email)
            else:
                raise HTTPException(status_code=400, detail="User exists")
        else:
            raise HTTPException(status_code=400, detail="Passwords do not match")
    else:
        raise HTTPException(status_code=400, detail="Enter a valid email")


@app.post("/login", tags=["Auth"])
async def login(user: UserLoginSchema):
    if await check_user(user):
        return sign_jwt(user.email)
    else:
        raise HTTPException(status_code=400, detail="Wrong credentials")


@app.get("/posts/{post_id}", dependencies=[Depends(JWTBearer())], tags=["Posts"])
async def retrieve_post(post_id):
    post = get_post(post_id)
    if post:
        return PostResponseSchema(id=post.id, author_id=post.author_id, content=post.content)
    else:
        raise HTTPException(status_code=404, detail="Post does not exist")


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["Posts"])
async def add_post(post: PostCreateSchema, jwt: str = Depends(JWTBearer())):
    user_mail = decode_jwt(jwt)["user_mail"]
    user_id = get_user(user_mail).id
    create_post(user_id, post.content)
    return {"message": "Post is created"}


@app.delete("/posts/{post_id}", dependencies=[Depends(JWTBearer())], tags=["Posts"])
async def remove_post(post_id: int, jwt: str = Depends(JWTBearer())):
    user_mail = decode_jwt(jwt)["user_mail"]
    user_id = get_user(user_mail).id
    post_author = get_post(post_id).author_id
    if user_id == post_author:
        if delete_post(post_id):
            return {"message": "Post is deleted"}
        else:
            raise HTTPException(status_code=400, detail="Post not found")
    else:
        raise HTTPException(status_code=403, detail="You cannot delete other users' posts")


@app.patch("/posts/{post_id}", dependencies=[Depends(JWTBearer())], tags=["Posts"])
async def edit_post(post_id: int, post: PostCreateSchema, jwt: str = Depends(JWTBearer())):
    user_mail = decode_jwt(jwt)["user_mail"]
    user_id = get_user(user_mail).id
    post_author = get_post(post_id).author_id
    if user_id == post_author:
        if update_post(post_id, post.content):
            return {"message": "Post is edited"}
        else:
            raise HTTPException(status_code=400, detail="Post not found")
    else:
        raise HTTPException(status_code=403, detail="You cannot edit other users' posts")


@app.post("/posts/{post_id}/rate", dependencies=[Depends(JWTBearer())], tags=["Likes"])
async def rate_post(post_id: int, rate: RatePostSchema, jwt: str = Depends(JWTBearer())):
    user_mail = decode_jwt(jwt)["user_mail"]
    user_id = get_user(user_mail).id
    post_author = get_post(post_id).author_id
    if user_id != post_author:
        if send_rate(user_id, post_id, rate.like):
            return {"message": "Post is rated"}
        else:
            raise HTTPException(status_code=400, detail="Post not found")
    else:
        raise HTTPException(status_code=403, detail="You cannot rate your own posts")


@app.delete("/posts/{post_id}/rate", dependencies=[Depends(JWTBearer())], tags=["Likes"])
async def remove_rate(post_id: int, jwt: str = Depends(JWTBearer())):
    user_mail = decode_jwt(jwt)["user_mail"]
    user_id = get_user(user_mail).id
    post_author = get_post(post_id).author_id
    if user_id != post_author:
        if delete_rate(user_id, post_id):
            return {"message": "Rate is removed"}
        else:
            raise HTTPException(status_code=400, detail="Post not found")
    else:
        raise HTTPException(status_code=403, detail="You cannot rate your own posts")
