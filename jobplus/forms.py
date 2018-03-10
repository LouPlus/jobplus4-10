from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,TextAreaField
from wtforms.validators import Length, Email, EqualTo, InputRequired,NumberRange,URL
from jobplus.models import db,User,Company
from wtforms import ValidationError


class CRegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(3, 24)])
    email = StringField('Email', validators=[InputRequired(), Email(message="请输入合法的email地址")])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
    def validate_name(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')
    def create_user(self):
        user=User(username=self.name.data,
                  email=self.email.data,
                  password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user


class URegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(3, 24)])
    email = StringField('Email', validators=[InputRequired(), Email(message="请输入合法的email地址")])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[InputRequired(), EqualTo('password')])
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
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 24)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')
    def validate_email(self,field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
    def validate_password(self,field):
        user=User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

class CompanyForm(FlaskForm):
    name=StringField('公司名称',validators=[InputRequired(),Length(5,32)])
    email=StringField('Email',validators=[InputRequired(),Email()])
    logo=StringField('图标',validators=[InputRequired(),URL()])
    user_id=IntegerField('联系人ID',validators=[InputRequired(),NumberRange(min=1,message='不存在该用户')])
    address=StringField('公司地址',validators=[InputRequired()])
    submit=SubmitField('提交')

    def validator_user_id(self,field):
        if not User.query.get(self.user_id.data):
            return ValidationError("用户不存在")

    def create_company(self):
        company=Company()
        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()
        return company

    def update_company(self,company):
        self.populate_obj(company)
        db.session.add(company)
        db.session.commit()
        return company

class UserProfileForm(FlaskForm):
    name=StringField('姓名',validators=[InputRequired()])
    email=StringField('Email',validators=[InputRequired(),Email()])
    password=PasswordField('密码',validators=[InputRequired(),Length(6,20)])
    phone=StringField('联系电话',validators=[InputRequired()])
    work_year=StringField('工作年限',validators=[InputRequired()])
    resume=StringField('简历地址')
    submit=SubmitField('提交')

    def valitator_phone(self,field):
        phone=self.field.data
        if phone[:2] not in ('13','15','18') and len(phone)!=11:
            raise ValidationError('无效的手机号码')

    def updated_profile(self,user):
        user.username=self.name.data
        user.email=self.email.data
        if self.password.data:
            user.password=self.password.data
        user.phone=self.phone.data
        user.work_year=self.work_year.data
        user.resume=self.resume.data
        db.session.add(user)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    name=StringField('公司名称',validators=[InputRequired()])
    email=StringField('Email',validators=[InputRequired(),Email()])
    address=StringField('公司地址',validators=[InputRequired()])
    password = PasswordField('密码', validators=[InputRequired(), Length(6, 20)])
    phone=StringField('电话')
    logo=StringField('Logo')
    fund=StringField('融资')
    scale=StringField('规模')
    filed=StringField('领域')
    detail=StringField('描述')
    submit=SubmitField('提交')

    def valitator_phone(self,field):
        phone=self.field.data
        if phone[:2] not in ('13','15','18') and len(phone)!=11:
            raise ValidationError('无效的手机号码')
    def upload_profile(self,user):
        user.username = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.detail:
            detail = user.detail
        else:
            detail = Company()
            detail.user_id = user.id
        self.populate_obj(detail)
        db.session.add(user)
        db.session.add(detail)
        db.session.commit()









