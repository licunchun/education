# 路由和视图函数 - 完整版本，包含数据库校验
from flask import render_template, redirect, url_for, flash, request, session
from education_system import app, db
from education_system.models.database import (
    User, Student, Teacher, Role, Course, OfferedCourse, CourseSelection, Grade,
    Major, Class, RegistrationApplication, ApplicationReview, Tuition, Payment
)
import hashlib
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
            'id': offered.id,  # 添加ID字段用于链接
            'name': course.name,
            'code': course.code,
            'credits': course.credits,
            'hours': course.hours,
            'course_type': course.course_type,
            'academic_year': offered.academic_year,
            'semester': offered.semester,
            'selected_count': offered.selected_count,
            'capacity': offered.capacity
        })
    
    return render_template('teacher/dashboard.html', title='教师控制面板', teacher=teacher_data, courses=courses_data)

# 管理员登录路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        password = request.form.get('password')
        
        if not admin_id or not password:
            flash('请输入管理员ID和密码', 'error')
            return render_template('admin/login.html', title='管理员登录')
        
        # 查找管理员用户
        user = User.query.filter_by(username=admin_id).first()
        if user and user.role and user.role.name == 'admin':
            # 验证密码
            if user.password == hash_password(password):
                if user.status:  # 检查账户是否启用
                    session['user_id'] = user.id
                    session['admin_id'] = user.username
                    session['user_type'] = 'admin'
                    session['real_name'] = user.real_name
                    flash(f'欢迎，{user.real_name}！', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('账户已被禁用，请联系系统管理员', 'error')
            else:
                flash('管理员ID或密码错误', 'error')
        else:
            flash('管理员ID或密码错误', 'error')
    
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
    return redirect(url_for('index'))

# 注册功能路由
@app.route('/register/student', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        try:            # 获取表单数据
            data = {
                'application_type': 'student',
                'name': request.form.get('name'),
                'gender': request.form.get('gender'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'birth_date': datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date(),
                'hometown': request.form.get('hometown'),
                'major_id': int(request.form.get('major_id')),
                'guardian_name': request.form.get('guardian_name'),
                'guardian_phone': request.form.get('guardian_phone'),
                'address': request.form.get('address'),
                'special_notes': request.form.get('special_notes', '')
            }
            
            # 验证手机号是否已存在（使用手机号替代身份证号进行重复检查）
            existing_app = RegistrationApplication.query.filter_by(
                phone=data['phone'],
                application_type='student'
            ).first()
            if existing_app:
                flash('该手机号已提交过学生注册申请', 'error')
                return redirect(url_for('student_register'))
            
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
        try:            # 获取表单数据
            data = {
                'application_type': 'teacher',
                'name': request.form.get('real_name'),
                'gender': request.form.get('gender'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'major_field': request.form.get('major_field'),
                'title': request.form.get('title'),
                'department': request.form.get('college'),
                'work_experience': request.form.get('work_experience'),
                'specialties': request.form.get('specialties'),
                'special_notes': request.form.get('special_notes', '')
            }
            
            # 验证手机号是否已存在（使用手机号替代身份证号进行重复检查）
            existing_app = RegistrationApplication.query.filter_by(
                phone=data['phone'],
                application_type='teacher'
            ).first()
            if existing_app:
                flash('该手机号已提交过教师注册申请', 'error')
                return redirect(url_for('teacher_register'))
            
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
    else:        # 显示状态查询页面
        if request.method == 'POST':
            app_id = request.form.get('app_id')
            phone = request.form.get('phone')
            
            if app_id:
                application = RegistrationApplication.query.get(app_id)
            elif phone:
                application = RegistrationApplication.query.filter_by(
                    phone=phone
                ).first()
            else:
                flash('请输入申请编号或手机号', 'error')
                return render_template('register/application_status.html')
            
            if not application:
                flash('未找到相关申请记录', 'error')
                return render_template('register/application_status.html')
            
            return render_template('register/application_status.html',
                                 title='申请状态查询',
                                 application=application)
        
        return render_template('register/application_status.html',
                             title='申请状态查询')

# 学生功能路由
@app.route('/student/courses')
def student_courses():
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    
    # 获取已选课程
    selected_courses = db.session.query(
        OfferedCourse, Course, Teacher, CourseSelection
    ).join(Course, OfferedCourse.course_id == Course.id)\
     .join(Teacher, OfferedCourse.teacher_id == Teacher.id)\
     .join(CourseSelection, CourseSelection.offered_course_id == OfferedCourse.id)\
     .filter(CourseSelection.student_id == student_id)\
     .filter(CourseSelection.status == '已选')\
     .all()
    
    # 获取可选课程（未选的课程）
    selected_course_ids = [sc[0].id for sc in selected_courses]
    available_courses = db.session.query(
        OfferedCourse, Course, Teacher
    ).join(Course, OfferedCourse.course_id == Course.id)\
     .join(Teacher, OfferedCourse.teacher_id == Teacher.id)\
     .filter(~OfferedCourse.id.in_(selected_course_ids))\
     .all()
    
    # 格式化数据
    selected_data = []
    for offered, course, teacher, selection in selected_courses:
        selected_data.append({
            'id': offered.id,
            'course_name': course.name,
            'teacher_name': teacher.name,
            'credits': course.credits,
            'hours': course.hours,
            'course_type': course.course_type,
            'selection_time': selection.selection_time.strftime('%Y-%m-%d %H:%M'),
            'schedule': offered.schedule,
            'location': offered.location
        })
    
    available_data = []
    for offered, course, teacher in available_courses:
        available_data.append({
            'id': offered.id,
            'course_name': course.name,
            'teacher_name': teacher.name,
            'credits': course.credits,
            'hours': course.hours,
            'course_type': course.course_type,
            'schedule': offered.schedule,
            'location': offered.location,
            'capacity': offered.capacity,
            'selected_count': offered.selected_count,            'can_select': offered.selected_count < offered.capacity
        })
    
    return render_template('student/courses.html', 
                         title='选课系统',
                         selected_courses=selected_data, 
                         available_courses=available_data)

@app.route('/student/select_course/<int:course_id>', methods=['POST'])
def student_select_course(course_id):
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    
    # 检查课程是否存在
    offered_course = OfferedCourse.query.get_or_404(course_id)
    
    # 检查是否已选
    existing = CourseSelection.query.filter_by(
        student_id=student_id,
        offered_course_id=course_id,
        status='已选'
    ).first()
    
    if existing:
        flash('您已经选择了这门课程', 'warning')
        return redirect(url_for('student_courses'))
    
    # 检查容量
    if offered_course.selected_count >= offered_course.capacity:
        flash('课程已满，无法选课', 'error')
        return redirect(url_for('student_courses'))
    
    # 添加选课记录
    from datetime import datetime
    selection = CourseSelection(
        student_id=student_id,
        offered_course_id=course_id,
        selection_time=datetime.now(),
        status='已选'
    )
    
    # 更新选课人数
    offered_course.selected_count += 1
    
    db.session.add(selection)
    db.session.commit()
    
    flash('选课成功！', 'success')
    return redirect(url_for('student_courses'))

@app.route('/student/drop_course/<int:course_id>', methods=['POST'])
def student_drop_course(course_id):
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    
    # 查找选课记录
    selection = CourseSelection.query.filter_by(
        student_id=student_id,
        offered_course_id=course_id,
        status='已选'
    ).first()
    
    if not selection:
        flash('未找到选课记录', 'error')
        return redirect(url_for('student_courses'))
    
    # 更新状态为已退
    selection.status = '已退'
    
    # 减少选课人数
    offered_course = OfferedCourse.query.get(course_id)
    if offered_course.selected_count > 0:
        offered_course.selected_count -= 1
    
    db.session.commit()
    
    flash('退课成功！', 'success')
    return redirect(url_for('student_courses'))

@app.route('/student/grades')
def student_grades():
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    
    # 获取学生成绩信息
    grades = db.session.query(
        Grade, OfferedCourse, Course, Teacher
    ).join(OfferedCourse, Grade.offered_course_id == OfferedCourse.id)\
     .join(Course, OfferedCourse.course_id == Course.id)\
     .join(Teacher, OfferedCourse.teacher_id == Teacher.id)\
     .filter(Grade.student_id == student_id)\
     .order_by(OfferedCourse.academic_year.desc(), OfferedCourse.semester.desc())\
     .all()
    
    # 格式化成绩数据
    grades_data = []
    total_credits = 0
    total_grade_points = 0
    
    for grade, offered, course, teacher in grades:
        grade_info = {
            'course_code': course.code,
            'course_name': course.name,
            'teacher_name': teacher.name,
            'academic_year': offered.academic_year,
            'semester': offered.semester,
            'credits': course.credits,
            'regular_grade': grade.regular_grade or '--',
            'exam_grade': grade.exam_grade or '--',
            'final_grade': grade.final_grade or '--',
            'gpa': grade.gpa or '--',
            'status': grade.status
        }
        grades_data.append(grade_info)
        
        # 计算总学分和平均绩点
        if grade.final_grade and grade.gpa:
            total_credits += course.credits
            total_grade_points += grade.gpa * course.credits
    
    # 计算平均绩点
    average_gpa = 0
    if total_credits > 0:
        average_gpa = round(total_grade_points / total_credits, 2)
    
    # 统计信息
    stats = {
        'total_courses': len(grades_data),
        'total_credits': total_credits,
        'average_gpa': average_gpa,
        'passed_courses': len([g for g in grades_data if isinstance(g['final_grade'], (int, float)) and g['final_grade'] >= 60])
    }
    
    return render_template('student/grades.html', 
                         title='成绩查询',
                         grades=grades_data,
                         stats=stats)

# 教师功能路由
@app.route('/teacher/course_management')
def teacher_course_management():
    if 'teacher_id' not in session or session.get('user_type') != 'teacher':
        flash('请先登录', 'error')
        return redirect(url_for('teacher_login'))
    
    teacher_id = session['teacher_id']
    
    # 获取教师开设的课程
    offered_courses = db.session.query(
        OfferedCourse, Course
    ).join(Course, OfferedCourse.course_id == Course.id)\
     .filter(OfferedCourse.teacher_id == teacher_id)\
     .order_by(OfferedCourse.academic_year.desc(), OfferedCourse.semester.desc())\
     .all()
    
    # 格式化课程数据
    courses_data = []
    for offered, course in offered_courses:
        course_info = {
            'id': offered.id,
            'course_code': course.code,
            'course_name': course.name,
            'academic_year': offered.academic_year,
            'semester': offered.semester,
            'credits': course.credits,
            'hours': course.hours,
            'course_type': course.course_type,
            'schedule': offered.schedule,
            'location': offered.location,
            'capacity': offered.capacity,
            'selected_count': offered.selected_count,
            'utilization': round((offered.selected_count / offered.capacity) * 100, 1) if offered.capacity > 0 else 0
        }
        courses_data.append(course_info)
    
    return render_template('teacher/course_management.html', 
                         title='课程管理',
                         courses=courses_data)

@app.route('/teacher/course/<int:course_id>/students')
def teacher_view_students(course_id):
    if 'teacher_id' not in session or session.get('user_type') != 'teacher':
        flash('请先登录', 'error')
        return redirect(url_for('teacher_login'))
    
    teacher_id = session['teacher_id']
    
    # 验证该课程是否属于该教师
    offered_course = OfferedCourse.query.filter_by(id=course_id, teacher_id=teacher_id).first()
    if not offered_course:
        flash('您没有权限查看该课程', 'error')
        return redirect(url_for('teacher_course_management'))
    
    # 获取选课学生信息
    students = db.session.query(
        Student, CourseSelection, Course
    ).join(CourseSelection, Student.id == CourseSelection.student_id)\
     .join(OfferedCourse, CourseSelection.offered_course_id == OfferedCourse.id)\
     .join(Course, OfferedCourse.course_id == Course.id)\
     .filter(CourseSelection.offered_course_id == course_id)\
     .filter(CourseSelection.status == '已选')\
     .order_by(Student.id)\
     .all()
    
    # 格式化学生数据
    students_data = []
    for student, selection, course in students:
        # 获取该学生的成绩记录
        grade = Grade.query.filter_by(
            student_id=student.id,
            offered_course_id=course_id
        ).first()
        
        student_info = {
            'id': student.id,
            'name': student.name,            'major': student.major.name if student.major else '未设置',
            'selection_time': selection.selection_time.strftime('%Y-%m-%d %H:%M'),
            'regular_grade': grade.regular_grade if grade else None,
            'exam_grade': grade.exam_grade if grade else None,
            'final_grade': grade.final_grade if grade else None,
            'gpa': grade.gpa if grade else None,            'grade_status': grade.status if grade else '未录入'
        }
        students_data.append(student_info)
    
    # 课程信息
    course_info = {
        'id': offered_course.id,
        'name': course.name,
        'code': course.code,
        'academic_year': offered_course.academic_year,
        'semester': offered_course.semester,
        'schedule': offered_course.schedule,
        'location': offered_course.location
    }
    
    return render_template('teacher/students_list.html', 
                         title='学生名单',
                         course=course_info,
                         students=students_data)

@app.route('/teacher/grade_management')
def teacher_grade_management():
    if 'teacher_id' not in session or session.get('user_type') != 'teacher':
        flash('请先登录', 'error')
        return redirect(url_for('teacher_login'))
    
    teacher_id = session['teacher_id']
      # 获取教师开设的课程及成绩录入情况
    courses_with_grades = db.session.query(
        OfferedCourse, Course,
        db.func.count(db.distinct(db.case(
            (Grade.student_id.isnot(None), Grade.student_id)
        ))).label('graded_count'),
        db.func.count(db.distinct(CourseSelection.student_id)).label('total_students')
    ).join(Course, OfferedCourse.course_id == Course.id)\
     .outerjoin(CourseSelection, db.and_(
        CourseSelection.offered_course_id == OfferedCourse.id,
        CourseSelection.status == '已选'
     ))\
     .outerjoin(Grade, db.and_(
        Grade.offered_course_id == OfferedCourse.id,
        Grade.student_id == CourseSelection.student_id
     ))\
     .filter(OfferedCourse.teacher_id == teacher_id)\
     .group_by(OfferedCourse.id, Course.id)\
     .order_by(OfferedCourse.academic_year.desc(), OfferedCourse.semester.desc())\
     .all()
    
    # 格式化数据
    courses_data = []
    for offered, course, graded_count, total_students in courses_with_grades:
        course_info = {
            'id': offered.id,
            'course_code': course.code,
            'course_name': course.name,
            'academic_year': offered.academic_year,
            'semester': offered.semester,
            'total_students': total_students or 0,
            'graded_count': graded_count or 0,
            'grade_progress': round((graded_count or 0) / (total_students or 1) * 100, 1)
        }
        courses_data.append(course_info)
    
    return render_template('teacher/grade_management.html', 
                         title='成绩管理',
                         courses=courses_data)

@app.route('/teacher/course/<int:course_id>/input_grades', methods=['GET', 'POST'])
def teacher_input_grades(course_id):
    if 'teacher_id' not in session or session.get('user_type') != 'teacher':
        flash('请先登录', 'error')
        return redirect(url_for('teacher_login'))
    
    teacher_id = session['teacher_id']
    
    # 验证课程权限
    offered_course = OfferedCourse.query.filter_by(id=course_id, teacher_id=teacher_id).first()
    if not offered_course:
        flash('您没有权限管理该课程成绩', 'error')
        return redirect(url_for('teacher_grade_management'))
    
    if request.method == 'POST':
        # 处理成绩录入
        student_ids = request.form.getlist('student_id')
        regular_grades = request.form.getlist('regular_grade')
        exam_grades = request.form.getlist('exam_grade')
        
        updated_count = 0
        for i, student_id in enumerate(student_ids):
            try:
                regular = float(regular_grades[i]) if regular_grades[i] else None
                exam = float(exam_grades[i]) if exam_grades[i] else None
                
                # 计算总评成绩（平时30% + 考试70%）
                final_grade = None
                gpa = None
                if regular is not None and exam is not None:
                    final_grade = round(regular * 0.3 + exam * 0.7, 1)
                    # 计算绩点（100-90:4.0, 89-80:3.0, 79-70:2.0, 69-60:1.0, <60:0）
                    if final_grade >= 90:
                        gpa = 4.0
                    elif final_grade >= 80:
                        gpa = 3.0
                    elif final_grade >= 70:
                        gpa = 2.0
                    elif final_grade >= 60:
                        gpa = 1.0
                    else:
                        gpa = 0.0
                
                # 查找或创建成绩记录
                grade = Grade.query.filter_by(
                    student_id=student_id,
                    offered_course_id=course_id
                ).first()
                
                if not grade:
                    grade = Grade(
                        student_id=student_id,
                        offered_course_id=course_id,
                        input_teacher_id=teacher_id
                    )
                    db.session.add(grade)
                
                # 更新成绩
                grade.regular_grade = regular
                grade.exam_grade = exam
                grade.final_grade = final_grade
                grade.gpa = gpa
                grade.input_teacher_id = teacher_id
                grade.input_time = datetime.now()
                grade.status = '已录入'
                
                updated_count += 1
                
            except ValueError:
                continue
        
        db.session.commit()
        flash(f'成功录入 {updated_count} 条成绩记录', 'success')
        return redirect(url_for('teacher_grade_management'))
    
    # GET请求 - 显示成绩录入页面
    # 获取选课学生及其成绩
    students_grades = db.session.query(
        Student, CourseSelection, Grade
    ).join(CourseSelection, Student.id == CourseSelection.student_id)\
     .outerjoin(Grade, db.and_(
        Grade.student_id == Student.id,
        Grade.offered_course_id == course_id
     ))\
     .filter(CourseSelection.offered_course_id == course_id)\
     .filter(CourseSelection.status == '已选')\
     .order_by(Student.id)\
     .all()
    
    # 格式化数据
    students_data = []
    for student, selection, grade in students_grades:       
        student_info = {
            'id': student.id,
            'name': student.name,
            'major': student.major.name if student.major else '未设置',
            'regular_grade': grade.regular_grade if grade else '',
            'exam_grade': grade.exam_grade if grade else '',
            'final_grade': grade.final_grade if grade else '',
            'gpa': grade.gpa if grade else '',
            'status': grade.status if grade else '未录入'
        }
        students_data.append(student_info)
    
    # 课程信息
    course_info = {
        'id': offered_course.id,
        'name': offered_course.course.name,
        'code': offered_course.course.code,
        'academic_year': offered_course.academic_year,
        'semester': offered_course.semester
    }
    
    return render_template('teacher/input_grades.html', 
                         title='录入成绩',
                         course=course_info,
                         students=students_data)

# 管理员功能路由
@app.route('/admin/student_management')
def admin_student_management():
    if 'admin_id' not in session or session.get('user_type') != 'admin':
        flash('请先登录', 'error')
        return redirect(url_for('admin_login'))
    return "学生管理功能开发中..."

@app.route('/admin/teacher_management')
def admin_teacher_management():
    if 'admin_id' not in session or session.get('user_type') != 'admin':
        flash('请先登录', 'error')
        return redirect(url_for('admin_login'))
    return "教师管理功能开发中..."

@app.route('/admin/course_management')
def admin_course_management():
    if 'admin_id' not in session or session.get('user_type') != 'admin':
        flash('请先登录', 'error')
        return redirect(url_for('admin_login'))
    return "课程管理功能开发中..."

# 管理员审核注册申请
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
            db.session.flush()  # 获取用户ID              # 创建学生记录
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
                account_balance=0.0,  # 新注册学生账户余额初始化为0
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

def _generate_student_id():
    """生成学生学号"""
    # 简单的学号生成逻辑：年份 + 顺序号
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
    # 简单的工号生成逻辑：T + 年份 + 顺序号
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

# 学生学费缴纳功能
@app.route('/student/tuition')
def student_tuition():
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    
    # 获取学生信息
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        flash('学生信息不存在', 'error')
        return redirect(url_for('student_login'))
    
    # 获取学费信息
    tuitions = Tuition.query.filter_by(student_id=student_id).order_by(
        Tuition.academic_year.desc(), Tuition.semester.desc()
    ).all()
      # 格式化学费数据
    tuition_data = []
    total_unpaid = 0
    
    for tuition in tuitions:
        # 获取支付记录
        payments = Payment.query.filter_by(tuition_id=tuition.id).all()
        paid_amount = sum(p.amount for p in payments)
        remaining = tuition.amount - paid_amount
        
        tuition_info = {
            'id': tuition.id,
            'academic_year': tuition.academic_year,
            'semester': tuition.semester,
            'amount': tuition.amount,
            'paid_amount': paid_amount,
            'remaining': remaining,
            'due_date': tuition.deadline,
            'status': '已缴清' if remaining <= 0 else '未缴清',
            'is_overdue': tuition.deadline and tuition.deadline < datetime.now().date() and remaining > 0,
            'payments': [{
                'amount': p.amount,
                'payment_time': p.payment_time,
                'payment_method': p.payment_method,
                'transaction_id': p.transaction_id
            } for p in payments]
        }
        tuition_data.append(tuition_info)
        
        if remaining > 0:
            total_unpaid += remaining
    
    # 学生财务统计
    stats = {
        'account_balance': student.account_balance,
        'total_unpaid': total_unpaid,
        'can_pay': student.account_balance >= total_unpaid if total_unpaid > 0 else True
    }
    
    return render_template('student/tuition.html',
                         title='学费缴纳',
                         student=student,
                         tuitions=tuition_data,
                         stats=stats)

@app.route('/student/pay_tuition/<int:tuition_id>', methods=['POST'])
def student_pay_tuition(tuition_id):
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    
    # 获取学生和学费信息
    student = Student.query.filter_by(id=student_id).first()
    tuition = Tuition.query.filter_by(id=tuition_id, student_id=student_id).first()
    
    if not student or not tuition:
        flash('信息不存在', 'error')
        return redirect(url_for('student_tuition'))
    
    try:
        # 获取支付金额
        pay_amount = float(request.form.get('amount', 0))
        if pay_amount <= 0:
            flash('支付金额必须大于0', 'error')
            return redirect(url_for('student_tuition'))
        
        # 计算应付金额
        paid_amount = sum(p.amount for p in Payment.query.filter_by(tuition_id=tuition_id).all())
        remaining = tuition.amount - paid_amount
        
        if pay_amount > remaining:
            flash('支付金额不能超过应付金额', 'error')
            return redirect(url_for('student_tuition'))
        
        if pay_amount > student.account_balance:
            flash('账户余额不足', 'error')
            return redirect(url_for('student_tuition'))
        
        # 创建支付记录
        payment = Payment(
            tuition_id=tuition_id,
            amount=pay_amount,
            payment_time=datetime.now(),
            payment_method='账户余额',
            transaction_id=f'TXN{datetime.now().strftime("%Y%m%d%H%M%S")}{tuition_id}'
        )
        
        # 扣减学生账户余额
        student.account_balance -= pay_amount
        
        db.session.add(payment)
        db.session.commit()
        
        flash(f'成功缴费 ¥{pay_amount:.2f}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'缴费失败：{str(e)}', 'error')
    
    return redirect(url_for('student_tuition'))

@app.route('/student/recharge', methods=['GET', 'POST'])
def student_recharge():
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('请先登录', 'error')
        return redirect(url_for('student_login'))
    
    if request.method == 'POST':
        student_id = session['student_id']
        student = Student.query.filter_by(id=student_id).first()
        
        if not student:
            flash('学生信息不存在', 'error')
            return redirect(url_for('student_login'))
        
        try:
            # 获取充值金额
            recharge_amount = float(request.form.get('amount', 0))
            if recharge_amount <= 0:
                flash('充值金额必须大于0', 'error')
                return render_template('student/recharge.html', title='账户充值')
            
            if recharge_amount > 10000:
                flash('单次充值金额不能超过¥10,000', 'error')
                return render_template('student/recharge.html', title='账户充值')
            
            # 模拟支付成功，增加账户余额
            student.account_balance += recharge_amount
            db.session.commit()
            
            flash(f'充值成功！已向账户充值 ¥{recharge_amount:.2f}', 'success')
            return redirect(url_for('student_tuition'))
            
        except ValueError:
            flash('请输入有效的金额', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'充值失败：{str(e)}', 'error')
    
    return render_template('student/recharge.html', title='账户充值')