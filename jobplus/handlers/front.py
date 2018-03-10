from flask import Blueprint,render_template,url_for,redirect
from jobplus.forms import LoginForm,URegisterForm,CRegisterForm
from flask import flash
from flask_login import login_user,logout_user,login_required
from jobplus.models import User,Job,db

front=Blueprint('front',__name__)
@front.route('/')
def index():
    newest_jobs=Job.query.order_by(Job.created_at.desc()).limit(9)
    newest_companies=User.query.filter(
        User.role==User.ROLE_COMPANY).order_by(User.created_at.desc()).limit(8)
    return render_template('index.html',
                           active='index',
                           newest_jobs=newest_jobs,
                           newest_companies=newest_companies)

@front.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user.is_disable:
            flash('用户已被禁用')
            return redirect(url_for('front.login'))
        else:
            login_user(user,form.remember_me.data)
            next = 'user.profile'
            if user.is_admin:
                next ='admin.index'
            elif user.is_company:
                next='company.profile'
            return redirect(url_for(next))
    return render_template('login.html',form=form)

@front.route('/cregister',methods=['GET','POST'])
def cregister():
    form=CRegisterForm()
    form.name.label='企业名称'
    if form.validate_on_submit():
        company_user=form.create_user()
        company_user.role=User.ROLE_COMPANY
        db.session.add(company_user)
        db.session.commit()
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

