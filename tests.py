# type: ignore
import os

os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta

import unittest
from app import app, db
from app.models import User, Post

    
class SpacedResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln()  # Add a blank line

class SpacedRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return SpacedResult(self.stream, self.descriptions, self.verbosity)

class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_hashing(self):
        """Testing that password hashing"""
        u = User( username = 'semb', email='semb@mail.com' )
        u.set_password('123')
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('123'))
    
    def test_avatar(self):
        """Test for avatar creation"""
        u = User( username = 'john', email='john@example.com' )
        self.assertEqual(
            u.avatar(128), 
            ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128')
            )
        
    def test_follow(self):
        """Testin following logic"""
        
        # create users and add them to the db
        u1 = User(username='semb', email='semb@mail.com')
        u2 = User(username='mimi', email='mimi@mail.com')
        db.session.add_all([u1,u2])
        db.session.commit()
        
        # get followers and following for the user instances
        following = db.session.scalars(u1.following.select()).all()
        followers = db.session.scalars(u2.followers.select()).all()
        
        # assert expected results
        self.assertEqual(following, [])
        self.assertEqual(followers, [])
        
        # make user 1 follow user 2
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)
        
        # query for the users followers and following
        u1_following = db.session.scalars(u1.following.select()).all()
        u2_followers = db.session.scalars(u2.followers.select()).all()
        self.assertEqual(u1_following[0].username, 'mimi')
        self.assertEqual(u2_followers[0].username, 'semb')
        
        # test unfollowing logic
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)
        
    
    
    def test_follow_posts(self):
        """Testing that user sees posts from followed accounts including users posts"""
        
        # create the users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])
        
        # create the posts from users
        now = datetime.now(timezone.utc)
        p1 = Post( body='post from john', author=u1, timestamp=now + timedelta(seconds=1) )
        p2 = Post( body='post from susan', author=u2, timestamp=now + timedelta(seconds=4) )
        p3 = Post( body='post from mary', author=u3, timestamp=now + timedelta(seconds=3) )
        p4 = Post( body='post from david', author=u4, timestamp=now + timedelta(seconds=2) )
        
        db.session.add_all([ p1, p2, p3, p4 ])
        
        # set up followings
        u1.follow(u2) # john follows susan 
        u1.follow(u4) # john follows david
        u2.follow(u3) # susan follows mary
        u3.follow(u4) # mary follows david
        
        db.session.commit()
        
        # check the following posts of each user
        f1 = db.session.scalars(u1.following_posts()).all()
        f2 = db.session.scalars(u2.following_posts()).all()
        f3 = db.session.scalars(u3.following_posts()).all()
        f4 = db.session.scalars(u4.following_posts()).all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])



# run the testing suite        
if __name__ == "__main__":
    # unittest.main(verbosity=2)
    unittest.main( testRunner = SpacedRunner(verbosity=2) )