# 路由和视图函数 - 完整稳定版本
import hashlib
from flask import render_template, redirect, url_for, flash, request, session
from education_system import app, db
from education_system.models.database import (
    User, Student, Teacher, Role, Course, OfferedCourse, CourseSelection, Grade,
    Major, Class, RegistrationApplication, ApplicationReview, Tuition, Payment
)
from datetime import datetime

def hash_password(password):
    """简单的密码哈希函数"""
    return hashlib.md5(password.encode()).hexdigest()

# 首页路由
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='学籍管理系统 - 首页')

# 学生登录路由
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        password = request.form.get('password')
        
        if not student_id or not password:
            flash('请输入学号和密码', 'error')
            return render_template('student/login.html', title='学生登录')
        
        # 查找学生信息
        student = Student.query.filter_by(id=student_id).first()
        if student and student.user:
            # 验证密码
            if student.user.password == hash_password(password):
                if student.user.status:  # 检查账户是否启用
                    session['user_id'] = student.user.id
                    session['student_id'] = student.id
                    session['user_type'] = 'student'
                    session['real_name'] = student.name
                    flash(f'欢迎，{student.name}！', 'success')
                    return redirect(url_for('student_dashboard'))
                else:
                    flash('账户已被禁用，请联系管理员', 'error')
            else:
                flash('学号或密码错误', 'error')
        else:
            flash('学号或密码错误', 'error')
    
    return render_template('student/login.html', title='学生登录')

@app.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    # 获取学生信息
    student = Student.query.filter_by(id=session['student_id']).first()
    if not student:
        flash('学生信息不存在', 'error')
        return redirect(url_for('student_login'))
    
    # 准备模板数据
    student_data = {
        'id': student.id,
        'name': student.name,
        'major': student.major.name if student.major else '未设置'
    }
    
    return render_template('student/dashboard.html', title='学生控制面板', student=student_data)

# 教师登录路由
@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        password = request.form.get('password')
        
        if not teacher_id or not password:
            flash('请输入工号和密码', 'error')
            return render_template('teacher/login.html', title='教师登录')
        
        # 查找教师信息
        teacher = Teacher.query.filter_by(id=teacher_id).first()
        if teacher and teacher.user:
            # 验证密码
            if teacher.user.password == hash_password(password):
                if teacher.user.status:  # 检查账户是否启用
                    session['user_id'] = teacher.user.id
                    session['teacher_id'] = teacher.id
                    session['user_type'] = 'teacher'
                    session['real_name'] = teacher.name
                    flash(f'欢迎，{teacher.name}！', 'success')
                    return redirect(url_for('teacher_dashboard'))
                else:
                    flash('账户已被禁用，请联系管理员', 'error')
            else:
                flash('工号或密码错误', 'error')
        else:
            flash('工号或密码错误', 'error')
    
    return render_template('teacher/login.html', title='教师登录')

@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session or session.get('user_type') != 'teacher':
        flash('请先登录', 'error')
        return redirect(url_for('teacher_login'))
    
    # 获取教师信息
    teacher = Teacher.query.filter_by(id=session['teacher_id']).first()
    if not teacher:
        flash('教师信息不存在', 'error')
        return redirect(url_for('teacher_login'))
    
    # 准备模板数据
    teacher_data = {
        'id': teacher.id,
        'name': teacher.name,
        'department': teacher.college or '未设置',
        'title': teacher.title or '未设置'
    }
    
    # 获取教师开设的课程（简化版本，用于dashboard显示）
    courses = db.session.query(
        OfferedCourse, Course
    ).join(Course, OfferedCourse.course_id == Course.id)\
     .filter(OfferedCourse.teacher_id == teacher.id)\
     .limit(5)\
     .all()
    
    courses_data = []
    for offered, course in courses:
        courses_data.append({
            'id': offered.id,
            'name': course.name,
            'students': offered.selected_count
        })
    
    return render_template('teacher/dashboard.html', title='教师控制面板', teacher=teacher_data, courses=courses_data)

# 管理员登录路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        password = request.form.get('password')
        
        if not admin_id or not password:
            flash('请输入管理员账号和密码', 'error')
            return render_template('admin/login.html', title='管理员登录')
        
        # 查找管理员账户
        user = User.query.filter_by(username=admin_id).first()
        if user and user.role and user.role.name == 'admin':
            if user.password == hash_password(password):
                if user.status:
                    session['user_id'] = user.id
                    session['admin_id'] = user.username
                    session['user_type'] = 'admin'
                    session['real_name'] = user.real_name
                    flash(f'欢迎，{user.real_name}！', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('管理员账户已被禁用', 'error')
            else:
                flash('管理员账号或密码错误', 'error')
        else:
            flash('管理员账号或密码错误', 'error')
    
    return render_template('admin/login.html', title='管理员登录')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session or session.get('user_type') != 'admin':
        flash('请先登录', 'error')
        return redirect(url_for('admin_login'))
    
    # 获取统计数据
    stats = {
        'students_count': Student.query.count(),
        'teachers_count': Teacher.query.count(),
        'courses_count': Course.query.count(),
        'pending_approvals': RegistrationApplication.query.filter_by(status='待审核').count()
    }
    
    return render_template('admin/dashboard.html', title='管理员控制面板', stats=stats)

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    flash('已成功退出登录', 'info')
    return redirect(url_for('index'))

# 注册功能路由
@app.route('/register/student', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        try:
            # 获取表单数据
            data = {
                'name': request.form.get('name'),
                'gender': request.form.get('gender'),
                'birth_date': request.form.get('birth_date'),
                'hometown': request.form.get('hometown'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'address': request.form.get('address'),
                'major_id': request.form.get('major_id'),
                'application_time': datetime.now(),
                'application_type': 'student',
                'status': '待审核'
            }
            
            # 验证必填字段
            required_fields = ['name', 'gender', 'birth_date', 'phone', 'major_id']
            for field in required_fields:
                if not data.get(field):
                    flash(f'请填写{field}', 'error')
                    return redirect(url_for('student_register'))
            
            # 检查是否已有申请
            existing_app = RegistrationApplication.query.filter_by(
                phone=data['phone'],
                application_type='student'
            ).first()
            if existing_app:
                flash('该手机号已有申请记录，请查询申请状态', 'warning')
                return redirect(url_for('application_status'))
            
            # 创建申请记录
            application = RegistrationApplication(**data)
            db.session.add(application)
            db.session.commit()
            
            flash('学生注册申请提交成功！请等待管理员审核。', 'success')
            return redirect(url_for('application_status', app_id=application.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'申请提交失败：{str(e)}', 'error')
    
    # 获取可选专业
    majors = Major.query.all()
    return render_template('register/student_register.html', 
                         title='学生注册申请',
                         majors=majors)

@app.route('/register/teacher', methods=['GET', 'POST'])
def teacher_register():
    if request.method == 'POST':
        try:
            # 获取表单数据
            data = {
                'name': request.form.get('name'),
                'gender': request.form.get('gender'),
                'department': request.form.get('department'),
                'title': request.form.get('title'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'application_time': datetime.now(),
                'application_type': 'teacher',
                'status': '待审核'
            }
            
            # 验证必填字段
            required_fields = ['name', 'gender', 'department', 'phone']
            for field in required_fields:
                if not data.get(field):
                    flash(f'请填写{field}', 'error')
                    return redirect(url_for('teacher_register'))
            
            # 检查是否已有申请
            existing_app = RegistrationApplication.query.filter_by(
                phone=data['phone'],
                application_type='teacher'
            ).first()
            if existing_app:
                flash('该手机号已有申请记录，请查询申请状态', 'warning')
                return redirect(url_for('application_status'))
            
            # 创建申请记录
            application = RegistrationApplication(**data)
            db.session.add(application)
            db.session.commit()
            
            flash('教师注册申请提交成功！请等待管理员审核。', 'success')
            return redirect(url_for('application_status', app_id=application.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'申请提交失败：{str(e)}', 'error')
    
    return render_template('register/teacher_register.html', 
                         title='教师注册申请')

@app.route('/register/status', methods=['GET', 'POST'])
@app.route('/register/status/<int:app_id>')
def application_status(app_id=None):
    if app_id:
        # 查看指定申请状态
        application = RegistrationApplication.query.get_or_404(app_id)
        return render_template('register/application_status.html',
                             title='申请状态查询',
                             application=application)
    else:
        # 显示状态查询页面
        if request.method == 'POST':
            app_id = request.form.get('app_id')
            phone = request.form.get('phone')
            
            if app_id:
                application = RegistrationApplication.query.get(app_id)
            elif phone:
                application = RegistrationApplication.query.filter_by(phone=phone).first()
            else:
                flash('请输入申请编号或手机号', 'error')
                return render_template('register/application_status.html',
                                     title='申请状态查询')
            
            if not application:
                flash('未找到相关申请记录', 'error')
                return render_template('register/application_status.html',
                                     title='申请状态查询')
            
            return render_template('register/application_status.html',
                                 title='申请状态查询',
                                 application=application)
        
        return render_template('register/application_status.html',
                             title='申请状态查询')

# 简化的管理员功能
@app.route('/admin/applications')
def admin_applications():
    if 'admin_id' not in session or session.get('user_type') != 'admin':
        flash('请先登录', 'error')
        return redirect(url_for('admin_login'))
    
    # 获取所有待审核的申请
    applications = RegistrationApplication.query.order_by(
        RegistrationApplication.application_time.desc()
    ).all()
    
    return render_template('admin/application_approval.html',
                         title='注册申请审核',
                         applications=applications)

def _generate_student_id():
    """生成学生学号"""
    year = datetime.now().year
    last_student = Student.query.filter(
        Student.id.like(f'{year}%')
    ).order_by(Student.id.desc()).first()
    
    if last_student:
        last_number = int(last_student.id[-4:])
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f'{year}{new_number:04d}'

def _generate_teacher_id():
    """生成教师工号"""
    year = datetime.now().year
    last_teacher = Teacher.query.filter(
        Teacher.id.like(f'T{year}%')
    ).order_by(Teacher.id.desc()).first()
    
    if last_teacher:
        last_number = int(last_teacher.id[-3:])
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f'T{year}{new_number:03d}'

@app.route('/admin/application/<int:app_id>/approve', methods=['POST'])
def approve_application(app_id):
    if 'admin_id' not in session or session.get('user_type') != 'admin':
        flash('请先登录', 'error')
        return redirect(url_for('admin_login'))
    
    application = RegistrationApplication.query.get_or_404(app_id)
    
    if application.status != '待审核':
        flash('该申请已处理过', 'error')
        return redirect(url_for('admin_applications'))
    
    try:
        # 获取审核意见
        review_comments = request.form.get('review_comments', '')
        
        if application.application_type == 'student':
            # 创建学生账户
            student_id = _generate_student_id()
            
            # 创建用户账户
            user = User(
                username=student_id,
                password=hash_password('123456'),  # 默认密码
                real_name=application.name,
                role_id=1,  # 假设1是学生角色ID
                contact=application.phone,
                status=True
            )
            db.session.add(user)
            db.session.flush()  # 获取用户ID
            
            # 创建学生记录
            student = Student(
                id=student_id,
                name=application.name,
                gender=application.gender,
                birth_date=application.birth_date,
                hometown=application.hometown,
                enrollment_date=datetime.now().date(),
                major_id=application.major_id,
                phone=application.phone,
                email=application.email,
                address=application.address,
                status='在读',
                account_balance=0.0,
                user_id=user.id
            )
            db.session.add(student)
            
        elif application.application_type == 'teacher':
            # 创建教师账户
            teacher_id = _generate_teacher_id()
            
            # 创建用户账户
            user = User(
                username=teacher_id,
                password=hash_password('123456'),  # 默认密码
                real_name=application.name,
                role_id=2,  # 假设2是教师角色ID
                contact=application.phone,
                status=True
            )
            db.session.add(user)
            db.session.flush()  # 获取用户ID
            
            # 创建教师记录
            teacher = Teacher(
                id=teacher_id,
                name=application.name,
                gender=application.gender,
                college=application.department,
                title=application.title,
                contact=application.phone,
                user_id=user.id
            )
            db.session.add(teacher)
        
        # 更新申请状态
        application.status = '已通过'
        application.review_time = datetime.now()
        application.reviewer_id = session['admin_id']
        application.review_comments = review_comments
        
        db.session.commit()
        flash('申请已通过审核，账户创建成功', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'审核处理失败：{str(e)}', 'error')
    
    return redirect(url_for('admin_applications'))

@app.route('/admin/application/<int:app_id>/reject', methods=['POST'])
def reject_application(app_id):
    if 'admin_id' not in session or session.get('user_type') != 'admin':
        flash('请先登录', 'error')
        return redirect(url_for('admin_login'))
    
    application = RegistrationApplication.query.get_or_404(app_id)
    
    if application.status != '待审核':
        flash('该申请已处理过', 'error')
        return redirect(url_for('admin_applications'))
    
    try:
        # 获取拒绝理由
        review_comments = request.form.get('review_comments', '')
        
        # 更新申请状态
        application.status = '已拒绝'
        application.review_time = datetime.now()
        application.reviewer_id = session['admin_id']
        application.review_comments = review_comments
        
        db.session.commit()
        flash('申请已拒绝', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'操作失败：{str(e)}', 'error')
    
    return redirect(url_for('admin_applications'))
