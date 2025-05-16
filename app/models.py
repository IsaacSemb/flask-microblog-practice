from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = sa.Table(
    # name of the table
    "followers",
    
    # metadta of the table
    db.metadata,
    
    # columns of the table or field
    sa.Column( 'follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True  ),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True ),
)
notes = """

this is not declared as a class like the users and the post models/tables
It has no other asociated data other than the foreign keys of the user ids

in this setting both as foreign keys will cause a
compund primary key
remember in DB classes -- two columns data treated as a key

In esscence, the pair cant be duplicated
A user can follow another user twice

"""


class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username:so.Mapped[str]  = so.mapped_column(sa.String(64), index=True, unique=True)
    email:so.Mapped[str]  = so.mapped_column( sa.String(120), index=True, unique=True)
    password_hash:so.Mapped[Optional[str]]  = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    
    posts: so.WriteOnlyMapped['Post'] = so.relationship( back_populates = 'author')
    
    # internal python representation of followers and following logic
    
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers'
    )
    
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary = followers,
        primaryjoin = (followers.c.followed_id == id),
        secondaryjoin = (followers.c.follower_id == id),
        back_populates = 'following'
    )
    
    # ---------- FOLLOWING FUNCTIONALITY-----------
    
    def is_following(self, user:'User') -> bool :
        """
        Check if user is following another user
        """
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None
    
    def follow(self, user:'User') -> None :
        """
        Action for a user to follow another user
        """
        if not self.is_following(user):
            self.following.add(user)
    
    def unfollow(self, user:'User') -> None :
        """
        Action for a user to unfollow another user
        """
        if self.is_following(user):
            self.following.remove(user)
    
    def followers_count(self) -> Optional[int] :
        """
        Get the number of users who follow a user
        """
        query = (
            sa.select(sa.func.count())
            .select_from( 
                self.followers.select().subquery()
            )
        )
        return db.session.scalar(query)
    
    def following_count(self) -> Optional[int] :
        """
        Get the number of users a user is following
        """
        query = (
            sa.select( sa.func.count() )
            .select_from(
            self.following.select().subquery()
            )
        )
        return db.session.scalar(query)
    
    # ---------- FOLLOWING FUNCTIONALITY END-----------
    
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password:str):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password:str)->bool:
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    
    def avatar(self,size):
        digest = md5(
            self.email
            .lower()
            .encode('utf-8')
            ).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
    
class Post(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    body : so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp : so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc) )
    user_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    
    def __repr__(self):
        return f"<Post {self.body}>"

