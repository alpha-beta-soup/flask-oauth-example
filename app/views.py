from app import app, db, lm
from flask import (
    render_template,
    flash,
    redirect,
    session, # A Flask global: data stored in the session will be available during that request... and any future requests made by the same client
    url_for,
    request,
    g # A Flask global: a place to store and share data during the life of a request
)
from flask.ext.login import (
    login_user,
    logout_user,
    current_user
)
# from .forms import LoginForm
from .models import User
from .oauth import OAuthSignIn

@app.route('/')
@app.route('/index')
def index():
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template(
        'index.html', title='Home', user=g.user, posts=posts
    )

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not g.user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not g.user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None and g.user.is_authenticated:
#         # A user already logged in will not need to do a second
#         # login
#         return redirect(url_for('index'))
#     form = LoginForm()
#     valid = form.validate_on_submit()
#     if valid: # Do form processing
#         # Submitted data is present and valid
#
#         # flask.session, similar to flask.g
#         session['remember_me'] = form.remember_me.data
#
#         # # Flash: quick way to show a message on the next page
#         # # user is presented with
#         # flash(
#         #     'Login requested for OpenID="%s", remember_me=%s' % (
#         #         form.openid.data, str(form.remember_me.data)
#         #     )
#         # )
#
#         return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
#
#     else:
#         print("ERRO")
#         # No data yet submitted TODO issue an error message for failed validation
#         return render_template(
#             'login.html', title='Sign In', form=form,
#             providers=app.config['OPENID_PROVIDERS']
#         )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    '''Load a user from the database'''
    return User.query.get(int(id))

@app.before_request
def before_request():
    '''current_user global is set by Flask-Login; we copy it to the g global to
    have better access to it. Then, all requests will have access to the logged
    in user'''
    g.user = current_user

# @oid.after_login
# def after_login(resp):
#     '''resp: information returned by the openid provider'''
#     if resp.email is None or resp.email == "" or "@" not in resp.email:
#         flash('Invalid login. Please try again')
#         return redirect(url_for('login'))
#     user = User.query.filter_by(email=resp.email).first()
#     if user is None:
#         # New user!
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             # Some openid providers might not have a nickname
#             nickname = resp.email.split("@")[0]
#         user = User(nickname=nickname, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#     login_user(user, remember=session.pop('remember_me', False))
#     return redirect(request.args.get('next') or url_for('index'))
