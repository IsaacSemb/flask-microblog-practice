from  hashlib import md5

gravatar_url1 = 'https://www.gravatar.com/avatar/' + md5(b'semb@mail.com').hexdigest()

print(gravatar_url1)