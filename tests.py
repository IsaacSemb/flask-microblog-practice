# type: ignore
import os

os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta

import unittest
from app import app, db
from app.models import User, Post

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
        u = User(
            username = 'semb',
            email='semb@mail.com'            
            )
        u.set_password('123')
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('123'))



# run the testing suite        
if __name__ == "__main__":
    unittest.main(verbosity=2)