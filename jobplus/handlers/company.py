from flask import Blueprint,render_template,request,current_app,redirect,url_for
from jobplus.models import Company,User
from flask_login import login_required,current_user
from jobplus.forms import CompanyProfileForm
from flask import flash

company=Blueprint('company',__name__,url_prefix='/company')

@company.route('/')
def index():
    page=request.args.get('page',default=1,type=int)
    pagination=Company.query.pagination(
        page=page,
        per_page=current_app.get['INDEX_PER_PAGE'],
        error_out=False
     )
    return render_template('#',pagination=pagination)

@company.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('您不是企业用户','Warning')
        return redirect(url_for('front.index'))
    form=CompanyProfileForm(obj=current_user.company_detail)
    form.name.data=current_user.username
    form.email.data=current_user.email
    if form.validate_on_submit():
        form.upload_profile(current_user)
        flash('公司信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html',form=form)



@company.route('/<int:company_id>')
def detail(company_id):
    company=Company.query.get_or_404(company_id)
    return render_template('company/detail.html',company=company)



