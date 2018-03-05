from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required
from jobplus.models import db,User,Company
from wtforms import ValidationError


class CRegisterForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email(message="请输入合法的email地址")])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    address = StringField('Address', validators=[Required()])
    submit = SubmitField('Submit')
    def create_company(self):
       company=Company()
       company.name=self.name.data
       company.email=self.email.data
       company.password=self.password.data
       company.address=self.address.data
       db.session.add(company)
       db.session.commit()
       return company
    def validate_name(self,field):
        if Company.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已经存在')
    def validate_email(self,field):
        if Company.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

class URegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email(message="请输入合法的email地址")])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')
    def create_user(self):
        user=User()
        user.username=self.username.data
        user.email=self.email.data
        user.password=self.password.data
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')
    def validate_email(self,field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
    def validate_password(self,field):
        user=User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
