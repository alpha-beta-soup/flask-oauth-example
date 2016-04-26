When working through [this brilliant Flask tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database), there are a number of complaints from people that the example uses OpenID and has not been updated to use OAuth. Because it annoys me when people bitch and moan instead of just trying to work out something for themselves, this is just a version of the tutorial at Part IV, using OAuth1 for user registration. The modifications are based on the tutorial author's own [additional tutorial on OAuth](http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask). It's possible to add OAuth2 with Facebook easily if you want it. You can clone this repo and then get on with the tutorial, but I'd recommend that you try do it yourself first—it's a great way to get your hands dirty with Flask.

If you clone, you will need to edit `config.py`, adding your own Twitter keys.

There are a few changes from the tutorial structure, in particular not using a login.html template. These should not be major barrier as long as you're thinkin' when you're workin'.

```sh
source flask/bin/activate
python run.py
```

Database creation: `python db_create.py`

Database migration: `python db_migrate.py`

Database upgrade: `python db_upgrade.py`
