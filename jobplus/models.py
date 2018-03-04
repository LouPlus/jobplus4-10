from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


db=SQLAlchemy()

class Base(db.Model):
    __abstract__=True
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base,UserMixin):
    __tablename__='user'
   
    ROLE_USER=10 
    ROLE_COMPANY=20 
    ROLE_ADMIN=30 

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True,index=True,nullable=False)
    email=db.Column(db.String(32),unique=True,index=True,nullable=False)
    _password=db.Column('password',db.String(256),nullable=False)
    role=db.Column(db.SmallInteger,default=ROLE_USER)
    resume_url=db.Column(db.String(64))
    phone=db.Column(db.Integer)

    def __repr__(self):
        return '<User:{}>'.format(self.username)
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,orig_password):
        self._password=generate_password_hash(orig_password)
    def check_password(self,password):
        return check_password_hash(self._password,password)
    @property
    def is_admin(self):
        return self.role==self.ROLE_ADMIN
    @property
    def is_company(self):
         return self.role==self.ROLE_COMPANY

class Company(Base):
    __tablename__='company'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),unique=True,index=True,nullable=False) 
    email=db.Column(db.String(32),unique=True,index=True,nullable=False)
    address=db.Column(db.String(128),nullable=False)
    logo=db.Column(db.String(64))
    fund=db.Column(db.String(256)) 
    scale=db.Column(db.String(64))  
    filed=db.Column(db.String(128)) 
    detile=db.Column(db.String(64)) 
    def __repr__(self):
        return '<Company{}>'.format(self.name)
class Job(Base):
    __tablename__='job'
    id=db.Column(db.Integer,primary_key=True)
    jobname=db.Column(db.String(32),unique=True,index=True,nullable=False)  
    salary=db.Column(db.String(32),nullable=False)
    requir=db.Column(db.String(258),nullable=False)
    time=db.Column(db.String(64),nullable=False)
    def __repr__(self):
        return '<Job{}>'.format(self.jobname)
class Delivery(Base):
    __tablename__='delivery'
    STATUS_WAITING=1
    STATUS_REJECT=2
    STATUS_ACCEPT=3
    id=db.Column(db.Integer,primary_key=True)
    job_id=db.Column(db.Integer,db.ForeignKey('job.id',ondelete='SET NULL'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
    status=db.Column(db.SmallInteger,default=STATUS_WAITING)
    response=db.Column(db.String(256))

 
