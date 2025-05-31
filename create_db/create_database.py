#type: ignore
import os, sys
from datetime import datetime, timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.abspath(os.path.dirname(basedir))
# print(basedir)
# print(root_dir)

# Add to sys.path
if root_dir not in sys.path:
    sys.path.append(root_dir)


from app import app,db
from app.models import Post, User
from faker import Faker
import random

fake = Faker()

def create_fake_user(num=1):
    """
    Create a sample fake user to add to the database
    """
    
    fake_users = []
    usernames = []
    emails = []
    for i in range(num):
        # create fake user details
        fake_username = fake.user_name()
        fake_email = fake.email()
        fake_about_me = fake.sentence(nb_words= random.randint(3,13))
        
        usernames.append(fake_username)
        emails.append(fake_email)
        
        user = User(
            username = fake_username,
            email = fake_email,
            about_me = fake_about_me
            )
            
        user.set_password('123')
        
        # print(user.username)
        # print(user.email)
        # print(user.about_me)
        # print(user.password_hash)
        
        # print(user)
        
        
        if user.username not in usernames or user.email not in emails:
            continue
        
        fake_users.append(user)
        
    
    # print(usernames)
    # print(emails)
    # print(fake_users)
    db.session.add_all(fake_users)
    db.session.commit()


def create_fake_timetamp():
    
    random_date = fake.date_time_between_dates(
                    datetime_start='-3y',
                    datetime_end='now'
                    )
    
    return random_date
    

def create_fake_post(min_posts=1, max_posts=10):
    
    # get all users to make them make posts
    all_users = db.session.query(User).all()

    all_posts = []
    
    for user in all_users:
        
        # select a number of posts you want the user to make
        number_of_posts_to_make =  random.randint(min_posts, max_posts)
        
        # create the actual posts        
        for _ in range(number_of_posts_to_make):
            
            # create the fake post
            fake_post = fake.text(max_nb_chars=random.randint(50, 180)).strip()
            
            # instantiate the post
            post = Post(
                body = fake_post,
                timestamp = create_fake_timetamp(),
                author = user
                )
            # add it to posts list
            all_posts.append(post)
    
    # add all posts and commit them
    db.session.add_all(all_posts)
    db.session.commit()
    


def create_fake_following(min_follow=0, max_follow=5):
    """Create a fake following mesh"""
    
    # get all users in the database
    all_users = db.session.query(User).all()
    # print(all_users)
    
    # Loop through the users
    for follower in all_users:
        # for each user set a random number of users they should follow
        number_of_people_to_follow = random.randint(min_follow, max_follow)
        
        # print(f"{follower} to follow {number_of_people_to_follow} users")
        # use the number to pick the number of all users they should follow
        list_of_users_to_follow = random.sample(k=number_of_people_to_follow, population=all_users) 
        
        #  make the follower follow the followee
        for followee in list_of_users_to_follow:
            follower.follow(followee)
    
    # commit all changes
    db.session.commit()
            
    
    
    

with app.app_context():
    
    print()
    
    sys.exit()
    
    # first drop all tables and recreate them
    db.drop_all()
    db.create_all()
    
    # create users
    create_fake_user(337)
    
    # create_fake_posts
    create_fake_post(min_posts=0, max_posts=127)
    
    # create followings
    create_fake_following(min_follow=0, max_follow=154)
    
    
    print()
    

