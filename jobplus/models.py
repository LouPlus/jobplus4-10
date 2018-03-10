from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask import url_for


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
    phone=db.Column(db.String(32))
    is_disable=db.Column(db.Boolean,default=False)
    detail = db.relationship('Company', uselist=False)
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
    detail=db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company_detail', uselist=False))
    def __repr__(self):
        return '<Company{}>'.format(self.name)
    @property
    def url(self):
        return url_for('company.detail',company_id=self.id)

class Job(Base):
    __tablename__='job'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),unique=True,index=True,nullable=False)
    salary_low=db.Column(db.Integer,nullable=False)
    salary_high=db.Column(db.Integer,nullable=False)
    location=db.Column(db.String(64))
    tags=db.Column(db.String(128))
    degree_requirment=db.Column(db.String(256))
    time=db.Column(db.String(64))
    is_open=db.Column(db.Boolean,default=False)
    company_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    company=db.relationship('User',uselist=False,backref=db.backref('jobs',lazy='dynamic'))
    view_count=db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Job{}>'.format(self.jobname)
    @property
    def tag_list(self):
        return self.tags.split(',')

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

 
