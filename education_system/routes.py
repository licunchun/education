# 路由和视图函数
from flask import render_template, redirect, url_for, flash, request, session
from education_system import app

# 首页路由
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='学籍管理系统 - 首页')

# 学生登录路由
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        # 这里应该有验证逻辑，暂时简化处理
        student_id = request.form.get('student_id')
        password = request.form.get('password')
        # TODO: 实现与数据库的验证
        if student_id and password:
            session['student_id'] = student_id
            session['user_type'] = 'student'
            return redirect(url_for('student_dashboard'))
        else:
            flash('账号或密码错误', 'error')
    return render_template('student/login.html', title='学生登录')
    
# 学生控制面板
@app.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('student_login'))
    # 模拟获取学生信息
    student = {
        'id': session['student_id'],
        'name': '张三',
        'major': '计算机科学与技术',
        'class_name': '计算机2023级1班'
    }
    return render_template('student/dashboard.html', title='学生控制面板', student=student)

# 教师登录路由
@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        password = request.form.get('password')
        # TODO: 实现与数据库的验证
        if teacher_id and password:
            session['teacher_id'] = teacher_id
            session['user_type'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('账号或密码错误', 'error')
    return render_template('teacher/login.html', title='教师登录')

# 教师控制面板
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('teacher_login'))
    # 模拟获取教师信息
    teacher = {
        'id': session['teacher_id'],
        'name': '李教授',
        'department': '计算机学院',
        'title': '副教授'
    }
    return render_template('teacher/dashboard.html', title='教师控制面板', teacher=teacher)

# 管理员登录路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        password = request.form.get('password')
        # TODO: 实现与数据库的验证
        if admin_id and password:
            session['admin_id'] = admin_id
            session['user_type'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            flash('账号或密码错误', 'error')
# 管理员控制面板
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    return render_template('admin/dashboard.html', title='管理员控制面板')

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
