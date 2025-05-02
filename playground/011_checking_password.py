import sys
from pathlib import Path

# Add the root folder to Python's path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Post


with app.app_context():
    sample_user = User(username='susan', email='susan@example.com')
    print(sample_user)
    
    sample_user.set_password('semb1234')
    
    print( sample_user.check_password('semb1234') )
    print( sample_user.check_password('semb12345') )

