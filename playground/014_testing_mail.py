# type: ignore
import sys
from pathlib import Path

# Add the root folder to Python's path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask_mail import Message
from app import mail, app

with app.app_context():
    msg = Message('test subject', sender=app.config['ADMINS'][0],
    recipients=['isaacsemb1996@gmail.com'])
    msg.body = 'text body'
    msg.html = '<h1>HTML body</h1>'
    mail.send(msg)