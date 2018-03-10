from flask import Blueprint,render_template,request,current_app,url_for,flash,redirect
from jobplus.decorator import admin_required
from jobplus.models import Company,db
from jobplus.forms import CompanyForm

admin=Blueprint('admin',__name__,url_prefix=('/admin'))

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/company')
@admin_required
def company():
    page=request.args.get('page',default=1,type=int)
    pagination=Company.query.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
            )
    return render_template('admin/company.html',pagination=pagination)

@admin.route('/company/create',methods=['GET','POST'])
@admin_required
def create_company():
    form=CompanyForm()
    if form.validate_on_submit():
        form.create_company()
        flash('公司创建成功','success')
        return redirect(url_for('admin.company'))
    return render_template('admin/create_company.html',form=form)

@admin.route('/company/<int:company_id>/edit',methods=['GET','POST'])
@admin_required
def edit_company(company_id):
    company=Company.query.get_or_404(company_id)
    form=CompanyForm(obj=company)
    if form.validate_on_submit():
        form.update_company(company)
        flash('公司更新成功','success')
        return redirect(url_for('admin.company'))
    return render_template('admin/edit_company.html',form=form,company=company)

@admin.route('/company/<int:company_id>/delete',methods=['GET','POST'])
@admin_required
def del_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('公司删除成功', 'success')
    return redirect(url_for('admin.company'))



