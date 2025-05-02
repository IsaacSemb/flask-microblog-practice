from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

hashed_pw = generate_password_hash('secret_password')
print(hashed_pw)

print( check_password_hash( hashed_pw, 'secret_password' ) )
print( check_password_hash( hashed_pw, 'my_secret_password' ) )

