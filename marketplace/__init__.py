#import flask - from the package import class
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.register_error_handler(404, page_not_found) #handles exceptions where the page does not exist
    app.secret_key='utroutoru'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///marketplace.sqlite'
    #initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)

    #the folder to store images
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    #from .models import User  # importing here to avoid circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import products
    app.register_blueprint(products.bp)

    from . import orders
    app.register_blueprint(orders.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    return app

# this function renders an error 404 page if the page does not exist within the directory. 
def page_not_found(e):
  return render_template('404.html'), 404



