from flask import Blueprint,render_template,url_for,redirect
from jobplus.forms import LoginForm,URegisterForm,CRegisterForm
from flask import flash
from flask_login import login_user,logout_user,login_required
from jobplus.models import User,Company

front=Blueprint('front',__name__)
@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        return redirect(url_for('front.index'))
    return render_template('login.html',form=form)

@front.route('/cregister',methods=['GET','POST'])
def cregister():
    form=CRegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录！','success')
        return redirect(url_for('front.login'))
    return render_template('company/register.html',form=form)

@front.route('/uregister',methods=['GET','POST'])
def uregister():
    form=URegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！','success')
        return redirect(url_for('front.login'))
    return render_template('user/register.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('安全退出','success')
    return redirect(url_for('front.index'))

front=Blueprint('front',__name__)
@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        return redirect(url_for('front.index'))
    return render_template('login.html',form=form)

@front.route('/cregister',methods=['GET','POST'])
def cregister():
    form=CRegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录！','success')
        return redirect(url_for('front.login'))
    return render_template('company/register.html',form=form)

@front.route('/uregister',methods=['GET','POST'])
def uregister():
    form=URegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！','success')
        return redirect(url_for('front.login'))
    return render_template('user/register.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('安全退出','success')
    return redirect(url_for('front.index'))

front=Blueprint('front',__name__)
@front.route('/')
def index():
    return render_template('index.html')
