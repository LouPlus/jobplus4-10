from flask import Flask,render_template
from jobplus.config import configs
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from jobplus.models import db,User,Company
from flask_login import LoginManager
 
def register_extensions(app):
    db.init_app(app)
    manager=Manager(app)
    Migrate(app,db)
    manager.add_command('db',MigrateCommand)
    login_manager=LoginManager()
    login_manager.init_app(app)
    #manager.run()
   
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)
    login_manager.login_view='front.login'

def register_blueprints(app):
    from .handlers import front,admin,user,job,company,test
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(job)
    app.register_blueprint(company)
    app.register_blueprint(test)

def create_app(config):
    app=Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprints(app)
    return app

