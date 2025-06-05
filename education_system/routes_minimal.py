# 路由和视图函数 - MySQL版本（SQLAlchemy 2.x兼容）
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from education_system import app, get_db
from sqlalchemy import text
import hashlib
from datetime import datetime

# 密码哈希函数
def hash_password(password):
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
        # 查询学生信息
        db = get_db()
        student = db.execute(
            text('SELECT s.*, u.password FROM students s JOIN users u ON s.user_id = u.id WHERE s.id = :student_id'),
            {'student_id': student_id}
        ).fetchone()
        
        if student and student['password'] == hash_password(password):
            session['student_id'] = student_id
            session['user_type'] = 'student'
            session['user_name'] = student['name']
            return redirect(url_for('student_dashboard'))
        
        flash('学号或密码错误', 'error')
    return render_template('student/login.html', title='学生登录')

# 学生控制面板
@app.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('student_login'))
    return render_template('student/dashboard.html', title='学生控制面板')

# 教师登录路由
@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        password = request.form.get('password')
        # 查询教师信息
        db = get_db()
        teacher = db.execute(
            text('SELECT t.*, u.password FROM teachers t JOIN users u ON t.user_id = u.id WHERE t.id = :teacher_id'),
            {'teacher_id': teacher_id}
        ).fetchone()
        
        if teacher and teacher['password'] == hash_password(password):
            session['teacher_id'] = teacher_id
            session['user_type'] = 'teacher'
            session['user_name'] = teacher['name']
            return redirect(url_for('teacher_dashboard'))
        
        flash('工号或密码错误', 'error')
    return render_template('teacher/login.html', title='教师登录')

# 教师控制面板
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('teacher_login'))
    return render_template('teacher/dashboard.html', title='教师控制面板')

# 管理员登录路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        password = request.form.get('password')
        # 查询管理员用户
        db = get_db()
        user = db.execute(
            text('SELECT * FROM users WHERE username = :admin_id AND role_id = 1'),
            {'admin_id': admin_id}
        ).fetchone()
        
        if user and user['password'] == hash_password(password):
            session['admin_id'] = admin_id
            session['user_type'] = 'admin'
            session['user_name'] = user['real_name']
            return redirect(url_for('admin_dashboard'))
        
        flash('管理员ID或密码错误', 'error')
    return render_template('admin/login.html', title='管理员登录')

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
