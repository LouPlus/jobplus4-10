from flask import Flask,render_template
from jobplus.config import configs
from jobplus.models import db,User,Job,Company,Delivery
 
def register_blueprint(app):
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
   db.init_app(app)
   register_blueprints(app)
   return app

