# 路由和视图函数 - SQLite版本
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from education_system import app, get_db
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
            'SELECT s.*, u.password FROM students s JOIN users u ON s.user_id = u.id WHERE s.id = ?',
            (student_id,)
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
    
    # 从数据库获取学生信息
    db = get_db()
    student = db.execute(
        '''SELECT s.*, m.name as major_name, c.name as class_name 
           FROM students s 
           LEFT JOIN majors m ON s.major_id = m.id 
           LEFT JOIN classes c ON s.class_id = c.id 
           WHERE s.id = ?''',
        (session['student_id'],)
    ).fetchone()
    
    if not student:
        session.clear()
        return redirect(url_for('student_login'))
    
    student_data = {
        'id': student['id'],
        'name': student['name'],
        'major': student['major_name'] or '未分配',
        'class_name': student['class_name'] or '未分配'
    }
    
    return render_template('student/dashboard.html', title='学生控制面板', student=student_data)

# 教师登录路由
@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        password = request.form.get('password')
        
        # 查询教师信息
        db = get_db()
        teacher = db.execute(
            'SELECT t.*, u.password FROM teachers t JOIN users u ON t.user_id = u.id WHERE t.id = ?',
            (teacher_id,)
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
    
    # 从数据库获取教师信息
    db = get_db()
    teacher = db.execute(
        'SELECT * FROM teachers WHERE id = ?',
        (session['teacher_id'],)
    ).fetchone()
    
    if not teacher:
        session.clear()
        return redirect(url_for('teacher_login'))
    
    # 获取教师开设的课程
    courses = db.execute(
        '''SELECT oc.*, c.name as course_name, c.credits, c.hours, c.course_type
           FROM offered_courses oc 
           JOIN courses c ON oc.course_id = c.id 
           WHERE oc.teacher_id = ?''',
        (teacher['id'],)
    ).fetchall()
    
    courses_data = []
    for course in courses:
        courses_data.append({
            'id': course['id'],
            'name': course['course_name'],
            'credits': course['credits'],
            'hours': course['hours'],
            'type': course['course_type'],
            'students_count': course['selected_count']
        })
    
    teacher_data = {
        'id': teacher['id'],
        'name': teacher['name'],
        'department': teacher['college'],
        'title': teacher['title']
    }
    
    return render_template('teacher/dashboard.html', title='教师控制面板', teacher=teacher_data, courses=courses_data)

# 管理员登录路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        password = request.form.get('password')
        
        # 查询管理员用户
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND role_id = 1',
            (admin_id,)
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
    
    # 获取统计数据
    db = get_db()
    students_count = db.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    teachers_count = db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0]
    courses_count = db.execute('SELECT COUNT(*) FROM courses').fetchone()[0]
    
    stats = {
        'students_count': students_count,
        'teachers_count': teachers_count,
        'courses_count': courses_count,
        'pending_approvals': 15  # 示例数据
    }
    
    return render_template('admin/dashboard.html', title='管理员控制面板', stats=stats)

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --------- 管理员功能路由 ---------- #

# 学生管理页面
@app.route('/admin/student_management')
def admin_student_management():
    if 'admin_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    # 获取所有学生
    db = get_db()
    students = db.execute(
        '''SELECT s.*, m.name as major_name, c.name as class_name 
           FROM students s 
           LEFT JOIN majors m ON s.major_id = m.id 
           LEFT JOIN classes c ON s.class_id = c.id''').fetchall()
    
    students_list = []
    for student in students:
        students_list.append({
            'id': student['id'],
            'name': student['name'],
            'gender': '男' if student['gender'] == 'M' else '女',
            'major': student['major_name'] or 'N/A',
            'class_name': student['class_name'] or 'N/A',
            'status': student['status']
        })
    
    majors = db.execute('SELECT * FROM majors').fetchall()
    classes = db.execute('SELECT * FROM classes').fetchall()
    
    return render_template('admin/student_management.html', title='学生管理', 
                          students=students_list, majors=majors, classes=classes)

# 教师管理页面
@app.route('/admin/teacher_management')
def admin_teacher_management():
    if 'admin_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    # 获取所有教师
    db = get_db()
    teachers = db.execute('SELECT * FROM teachers').fetchall()
    
    teachers_list = []
    for teacher in teachers:
        teachers_list.append({
            'id': teacher['id'],
            'name': teacher['name'],
            'gender': '男' if teacher['gender'] == 'M' else '女',
            'college': teacher['college'],
            'title': teacher['title'],
            'contact': teacher['contact']
        })
    
    return render_template('admin/teacher_management.html', title='教师管理', 
                          teachers=teachers_list)

# 课程管理页面
@app.route('/admin/course_management')
def admin_course_management():
    if 'admin_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    # 获取所有课程
    db = get_db()
    courses = db.execute('SELECT * FROM courses').fetchall()
    
    courses_list = []
    for course in courses:
        courses_list.append({
            'id': course['id'],
            'code': course['code'],
            'name': course['name'],
            'type': course['course_type'],
            'credits': course['credits'],
            'hours': course['hours'],
            'college': course['college']
        })
    
    # 获取所有开课信息
    offered_courses = db.execute(
        '''SELECT oc.*, c.name as course_name, t.name as teacher_name
           FROM offered_courses oc 
           JOIN courses c ON oc.course_id = c.id 
           JOIN teachers t ON oc.teacher_id = t.id''').fetchall()
    
    offered_list = []
    for oc in offered_courses:
        offered_list.append({
            'id': oc['id'],
            'course_name': oc['course_name'],
            'academic_year': oc['academic_year'],
            'semester': oc['semester'],
            'teacher_name': oc['teacher_name'],
            'schedule': oc['schedule'],
            'location': oc['location'],
            'selected': oc['selected_count'],
            'capacity': oc['capacity']
        })
    
    teachers = db.execute('SELECT * FROM teachers').fetchall()
    
    return render_template('admin/course_management.html', title='课程管理', 
                          courses=courses_list, offered_courses=offered_list, teachers=teachers)

# 添加学生
@app.route('/admin/add_student', methods=['POST'])
def add_student():
    if 'admin_id' not in session or session['user_type'] != 'admin':
        return jsonify({'status': 'error', 'message': '请先登录'}), 401
    
    # 获取表单数据
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    birth_date_str = request.form.get('birth_date')
    id_card = request.form.get('id_card')
    hometown = request.form.get('hometown')
    enrollment_date_str = request.form.get('enrollment_date')
    major_id = request.form.get('major_id')
    class_id = request.form.get('class_id')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    
    # 检查学号是否已存在
    db = get_db()
    existing = db.execute('SELECT id FROM students WHERE id = ?', (student_id,)).fetchone()
    if existing:
        return jsonify({'status': 'error', 'message': '学号已存在'}), 400
    
    try:
        # 创建用户
        db.execute(
            'INSERT INTO users (username, password, real_name, role_id, contact) VALUES (?, ?, ?, ?, ?)',
            (student_id, hash_password('123456'), name, 3, phone)
        )
        user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # 创建学生记录
        db.execute(
            '''INSERT INTO students (id, name, gender, birth_date, id_card, hometown, 
                                   enrollment_date, major_id, class_id, phone, email, 
                                   address, status, user_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (student_id, name, gender, birth_date_str, id_card, hometown, 
             enrollment_date_str, major_id, class_id, phone, email, address, '在读', user_id)
        )
        
        db.commit()
        return jsonify({'status': 'success', 'message': '学生添加成功'})
        
    except Exception as e:
        db.rollback()
        return jsonify({'status': 'error', 'message': f'添加失败: {str(e)}'}), 500

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
