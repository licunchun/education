from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 从主应用导入db实例
from education_system import db

# 用户角色表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100))
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f'<Role {self.name}>'

# 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    real_name = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    contact = db.Column(db.String(50))
    status = db.Column(db.Boolean, default=True)  # True表示启用，False表示禁用
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<User {self.username}>'

# 学生表
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(20), primary_key=True)  # 学号
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1))  # 'M'表示男，'F'表示女
    birth_date = db.Column(db.Date)
    id_card = db.Column(db.String(18), unique=True)
    hometown = db.Column(db.String(100))
    enrollment_date = db.Column(db.Date)
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    photo_path = db.Column(db.String(200))
    status = db.Column(db.String(20), default='在读')  # 在读/毕业/休学/退学
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    # 关联关系
    user = db.relationship('User', backref=db.backref('student', uselist=False))
    major = db.relationship('Major', backref='students')
    class_obj = db.relationship('Class', backref='students')
    grades = db.relationship('Grade', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.id} {self.name}>'

# 专业表
class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    college = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, default=4)  # 学制年限
    
    def __repr__(self):
        return f'<Major {self.name}>'

# 班级表
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))
    grade_year = db.Column(db.Integer)  # 年级
    advisor_id = db.Column(db.String(20), db.ForeignKey('teachers.id'))
    
    # 关联关系
    major = db.relationship('Major', backref='classes')
    advisor = db.relationship('Teacher', backref='advised_classes')
    
    def __repr__(self):
        return f'<Class {self.name}>'

# 教师表
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.String(20), primary_key=True)  # 工号
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1))
    college = db.Column(db.String(50))
    title = db.Column(db.String(20))  # 职称
    contact = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    # 关联关系
    user = db.relationship('User', backref=db.backref('teacher', uselist=False))
    offered_courses = db.relationship('OfferedCourse', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f'<Teacher {self.id} {self.name}>'

# 课程表
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    course_type = db.Column(db.String(20), default='选修')  # 必修/选修
    credits = db.Column(db.Float, nullable=False)  # 学分
    hours = db.Column(db.Integer, nullable=False)  # 学时
    college = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    # 关联关系
    offered_courses = db.relationship('OfferedCourse', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.code} {self.name}>'

# 开课信息表
class OfferedCourse(db.Model):
    __tablename__ = 'offered_courses'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)  # 如 2023-2024
    semester = db.Column(db.String(20), nullable=False)  # 如 第一学期
    teacher_id = db.Column(db.String(20), db.ForeignKey('teachers.id'), nullable=False)
    schedule = db.Column(db.String(100))  # 上课时间
    location = db.Column(db.String(100))  # 上课地点
    capacity = db.Column(db.Integer, default=60)  # 课程容量
    selected_count = db.Column(db.Integer, default=0)  # 已选人数
    
    # 关联关系
    grades = db.relationship('Grade', backref='offered_course', lazy=True)
    
    def __repr__(self):
        return f'<OfferedCourse {self.course_id} {self.academic_year} {self.semester}>'

# 选课记录表
class CourseSelection(db.Model):
    __tablename__ = 'course_selections'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.id'), nullable=False)
    offered_course_id = db.Column(db.Integer, db.ForeignKey('offered_courses.id'), nullable=False)
    selection_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='已选')  # 已选/已退
    
    # 关联关系
    student = db.relationship('Student', backref='course_selections')
    offered_course = db.relationship('OfferedCourse', backref='course_selections')
    
    def __repr__(self):
        return f'<CourseSelection {self.student_id} {self.offered_course_id}>'

# 成绩表
class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.id'), nullable=False)
    offered_course_id = db.Column(db.Integer, db.ForeignKey('offered_courses.id'), nullable=False)
    regular_grade = db.Column(db.Float)  # 平时成绩
    exam_grade = db.Column(db.Float)  # 考试成绩
    final_grade = db.Column(db.Float)  # 总评成绩
    gpa = db.Column(db.Float)  # 绩点
    input_time = db.Column(db.DateTime, default=datetime.now)
    input_teacher_id = db.Column(db.String(20), db.ForeignKey('teachers.id'))
    status = db.Column(db.String(20), default='未审核')  # 未审核/已审核
    
    # 关联关系
    input_teacher = db.relationship('Teacher', foreign_keys=[input_teacher_id], backref='input_grades')
    
    def __repr__(self):
        return f'<Grade {self.student_id} {self.offered_course_id} {self.final_grade}>'

# 学费表
class Tuition(db.Model):
    __tablename__ = 'tuitions'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='未缴费')  # 未缴费/部分缴费/已缴费
    deadline = db.Column(db.Date)
    
    # 关联关系
    student = db.relationship('Student', backref='tuitions')
    payments = db.relationship('Payment', backref='tuition', lazy=True)
    
    def __repr__(self):
        return f'<Tuition {self.student_id} {self.academic_year} {self.status}>'

# 支付记录表
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    tuition_id = db.Column(db.Integer, db.ForeignKey('tuitions.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_time = db.Column(db.DateTime, default=datetime.now)
    payment_method = db.Column(db.String(20))  # 支付方式
    transaction_id = db.Column(db.String(50))  # 交易号
    
    def __repr__(self):
        return f'<Payment {self.tuition_id} {self.amount}>'

# 注册申请表
class RegistrationApplication(db.Model):
    __tablename__ = 'registration_applications'
    id = db.Column(db.Integer, primary_key=True)
    application_type = db.Column(db.String(20), nullable=False)  # 'student' or 'teacher'
    
    # 通用字段
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1))
    id_number = db.Column(db.String(18), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    
    # 学生专用字段
    birth_date = db.Column(db.Date)
    hometown = db.Column(db.String(100))
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    guardian_name = db.Column(db.String(50))
    guardian_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # 教师专用字段
    major_field = db.Column(db.String(100))
    title = db.Column(db.String(50))
    department = db.Column(db.String(100))
    work_experience = db.Column(db.Text)
    specialties = db.Column(db.Text)
    
    # 通用字段
    special_notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='待审核')  # 待审核/已通过/已拒绝
    application_time = db.Column(db.DateTime, default=datetime.now)
    review_time = db.Column(db.DateTime)
    reviewer_id = db.Column(db.String(50), db.ForeignKey('users.username'))
    review_comments = db.Column(db.Text)
    
    # 关联关系
    major = db.relationship('Major', backref='applications')
    class_obj = db.relationship('Class', backref='applications')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviewed_applications')
    
    def __repr__(self):
        return f'<RegistrationApplication {self.id} {self.name} {self.application_type}>'

# 申请审核记录表
class ApplicationReview(db.Model):
    __tablename__ = 'application_reviews'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('registration_applications.id'), nullable=False)
    reviewer_id = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)
    review_action = db.Column(db.String(20), nullable=False)  # 'approve', 'reject', 'request_info'
    review_comments = db.Column(db.Text)
    review_time = db.Column(db.DateTime, default=datetime.now)
    
    # 关联关系
    application = db.relationship('RegistrationApplication', backref='reviews')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='review_records')
    
    def __repr__(self):
        return f'<ApplicationReview {self.application_id} {self.review_action}>'
