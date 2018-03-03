from flask import Flask,render_template
  2 from jobplus.config import configs
  3 from jobplus.models import db,User,Job,Company
  4 
  5 def create_app(config):
  6     app=Flask(__name__)
  7     app.config.from_object(configs.get(config))
  8     db.init_app(app)
  9     
 10     @app.route('/')
 11     def index():
 12         return render_template('index.html')
 13     return app

