# type:ignore
from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, request, url_for
from app import app, db, login_manager

from app.forms import (
    LoginForm,
    RegistrationForm,
    EditProfileForm,
    EmptyForm,
    PostForm
    )


from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Post
import sqlalchemy as sa



# this is used to get the context of the user
@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))


# to protect a view from people who arent logged in 
# you use the login required decorator
#  @login_required below the route decorator
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    """ 
    This is the home page to the application  
    It displays current state of the users and latest posts
    """
    
    # form for making a post
    form = PostForm()
    
    # processing of the form data
    if form.validate_on_submit():
        post = Post( 
                    body = form.post.data,
                    author = current_user
                    )
        db.session.add(post)
        db.session.commit()
        flash("Your Post is now live!")
        return redirect(url_for('index'))
    
    # implement pagination
    page = request.args.get('page',1, type=int)
    
    
    # original
    # posts = db.session.scalars(current_user.following_posts()).all()
    
    # paginated
    posts = db.paginate( 
                        current_user.following_posts(),
                        page=page,
                        per_page=app.config['POSTS_PER_PAGE'],
                        error_out=False                    
                    )
    
    # Compute if there are next and previous pages url
    # so that we can pass them down too
    
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    
    
    return render_template( 
                            'index.html',
                            title='Home Page',
                            posts=posts.items,
                            form=form,
                            next_url = next_url,
                            prev_url = prev_url
                        )


@app.route('/explore')
@login_required
def explore():
    """
    This view return a stream of all posts from users in the system
    so that the current user can see them and follow them etc
    """
    
    # implement pagination
    page = request.args.get('page',1, type=int)
    
    
    # select all posts in the system and order them by newest
    query = (
        sa
        .select(Post)
        .order_by(Post.timestamp.desc())
    )
    posts = db.paginate(
        query,
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    
    # Compute if there are next and previous pages url
    # so that we can pass them down too
    
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    
    # this reuses the index template since they some what serve a similar purpose
    # the only difference is here we dont serve a post form for posting stuff
    return render_template( 
                            'index.html',
                            title='Explore',
                            posts=posts.items,
                            next_url = next_url,
                            prev_url = prev_url
                            )



@app.route('/register', methods=[ 'GET', 'POST' ])
def register():
    
    # if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # pullin the registration form from forms    
    register_form = RegistrationForm()
    
    if register_form.validate_on_submit():
        
        # if valid, create the user
        user = User(
            username=register_form.username.data,
            email=register_form.email.data            
            )
        
        # set the user password
        user.set_password(register_form.password.data)
        
        # add user to the db and commit them
        db.session.add(user)
        db.session.commit()
        
        # send notification to the front end
        flash('Successfully registered')
        
        # send them to login page
        return redirect(url_for('index'))
    
    # if something goes wrong re render the register page
    return render_template( 'register.html', title='Register', form = register_form)


@app.route('/login', methods=[ 'GET', 'POST' ])
def login():
    
    # checked if the user is authenticated already
    # An already logged in user should not go to the login page
    if current_user.is_authenticated:
        return  redirect(url_for('index'))
    
    # pass the login form to the view
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        
        # check for user details from submitted form in the database
        user = db.session.scalar(
            sa
            .select(User)
            .where(User.username==login_form.username.data)
        )
        
        # check password if the user exists
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # if sucessfull if statement wont run
        login_user(user, remember=login_form.remember_me.data)
        
        # Incase the user came from a formerly requested page, we want to send them back 
        # basically the applcation being smart
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
            
        # send the user to the homepage
        return redirect(url_for('index'))
    
    return render_template('login.html', title="Sign In", form=login_form )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# User profile view



@app.route('/user/<username>')
@login_required
def user(username):
    # get user object or 404 not found
    user = db.first_or_404( sa
                            .select(User)
                            .where(User.username==username)
                            )
    
    # implement pagination
    page = request.args.get('page', 1, type='int')
    
    # get all users posts 
    query = (user
            .posts
            .select()
            .order_by(Post.timestamp.desc())
            )
        
    # Get the post from this user and display the mto the user
    posts = db.paginate(
        query,
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    
    
    # Compute if there are next and previous pages url
    # so that we can pass them down too
    
    next_url = url_for('user',username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user',username=user.username, page=posts.prev_num) if posts.has_prev else None

    
    # instantiate follow/unfollow form
    form = EmptyForm()
    
    return render_template( 
                        'user.html',
                        user=user,
                        posts=posts.items,
                        form=form,
                        prev_url=prev_url,
                        next_url=next_url
                        )

# to be done before every request
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    # present the form
    edit_form = EditProfileForm(current_user.username)
    
    # validate form
    if edit_form.validate_on_submit():
        current_user.username = edit_form.username.data
        current_user.about_me = edit_form.about_me.data
        db.session.commit()
        flash("Your changed have been saved")
        return redirect( url_for('index') )
        
    elif request.method == 'GET':
        edit_form.username.data = current_user.username 
        edit_form.about_me.data = current_user.about_me
        

    return render_template( 'edit_profile.html', form=edit_form, title="Edit Profile" )

@app.route('/follow/<username>', methods = ['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    
    if form.validate_on_submit():
        
        user = db.session.scalar(
            sa.select(User)
            .where(User.username == username)
        )
        
        if user is None:
            flash(f'User not found!')
            return redirect(url_for('index'))
        
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username = username ))
        
        current_user.follow(user)
        flash(f"Youre now following {username}!")
        return redirect(url_for('user', username = username ))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods = ['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    
    if form.validate_on_submit():
        
        user = db.session.scalar(
            sa.select(User)
            .where(User.username == username)
        )
        
        if user is None:
            flash(f'User not found!')
            return redirect(url_for('index'))
        
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username = username ))
        
        current_user.unfollow(user)
        flash(f"Youre have unfollowed {username}!")
        return redirect(url_for('user', username = username ))
    else:
        return redirect(url_for('index'))


    
    
    
    