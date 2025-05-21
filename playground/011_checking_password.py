# type: ignore
import sys
from pathlib import Path

# Add the root folder to Python's path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Post


# TESTING OUT A PASSWORD
def test_password():
    with app.app_context():
        sample_user = User(username='susan', email='susan@example.com')
        print(sample_user)
        
        sample_user.set_password('semb1234')
        
        print( sample_user.check_password('semb1234') )
        print( sample_user.check_password('semb12345') )


# creating a fake user 
def create_fake_user( u_name,email, p_word):
    with app.app_context():
        test_user = User(username=u_name, email=email)
        
        test_user.set_password(p_word)
        db.session.add(test_user)
        db.session.commit()
        
create_fake_user(
    u_name='semb',
    email="semb@mail.com",
    p_word='123'
)