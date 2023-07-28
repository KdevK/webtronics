from data.models import (
    session_maker,
    User, Post, Rate,
)


def get_user(email_: str) -> User:
    with session_maker() as db:
        try:
            user = db.query(User).filter(User.email == email_).first()
            return user
        except Exception as e:
            raise e


def create_user(email_: str, password: str) -> User | None:
    with session_maker() as db:
        user = db.query(User).filter(User.email == email_).first()
        if user is None:
            user = User(email=email_, password=password)
            db.add(user)
            db.commit()
            return user
        return None


def get_post(post_id) -> Post | None:
    with session_maker() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            return post
        return None


def create_post(author_id, content) -> Post:
    with session_maker() as db:
        post = Post(author_id=author_id, content=content)
        db.add(post)
        db.commit()
    return post


def delete_post(post_id) -> bool:
    with session_maker() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            db.delete(post)
            db.commit()
            return True
        return False


def update_post(post_id, content) -> bool:
    with session_maker() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            post.content = content
            db.commit()
            return True
        return False


def send_rate(user_id, post_id, like) -> bool:
    with session_maker() as db:
        rate = db.query(Rate).filter(Rate.user_id == user_id, Rate.post_id == post_id).first()
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            if rate:
                rate.like = like
            else:
                rate = Rate(user_id=user_id, post_id=post_id, like=like)
                db.add(rate)
                db.commit()
            return True
        return False


def delete_rate(user_id, post_id) -> bool:
    with session_maker() as db:
        rate = db.query(Rate).filter(Rate.user_id == user_id, Rate.post_id == post_id).first()
        if rate:
            db.delete(rate)
            db.commit()
            return True
        return False
