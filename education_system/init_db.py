import sqlite3
import hashlib
from datetime import datetime, date
from education_system import app, get_db

def hash_password(password):
    """简单的密码哈希函数"""
    return hashlib.md5(password.encode()).hexdigest()

def init_db():
    """初始化数据库并添加测试数据"""    # 首先初始化数据库结构
    with app.app_context():
        db = get_db()
        import os
        schema_path = os.path.join(app.root_path, 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            db.executescript(f.read())
        
        # 添加角色
        db.execute('INSERT INTO roles (name, description) VALUES (?, ?)', ('admin', '系统管理员'))
        db.execute('INSERT INTO roles (name, description) VALUES (?, ?)', ('teacher', '教师'))
        db.execute('INSERT INTO roles (name, description) VALUES (?, ?)', ('student', '学生'))
        
        # 添加管理员用户
        db.execute(
            'INSERT INTO users (username, password, real_name, role_id, contact) VALUES (?, ?, ?, ?, ?)',
            ('admin001', hash_password('admin123'), '张管理', 1, 'admin@school.edu.cn')
        )
        
        # 添加专业
        db.execute(
            'INSERT INTO majors (code, name, college, duration) VALUES (?, ?, ?, ?)',
            ('CS001', '计算机科学与技术', '计算机学院', 4)
        )
        db.execute(
            'INSERT INTO majors (code, name, college, duration) VALUES (?, ?, ?, ?)',
            ('SE001', '软件工程', '计算机学院', 4)
        )
        db.execute(
            'INSERT INTO majors (code, name, college, duration) VALUES (?, ?, ?, ?)',
            ('MA001', '数学', '理学院', 4)
        )
        
        # 添加教师用户和教师信息
        db.execute(
            'INSERT INTO users (username, password, real_name, role_id, contact) VALUES (?, ?, ?, ?, ?)',
            ('t001', hash_password('teacher123'), '李教授', 2, 'teacher1@school.edu.cn')
        )
        teacher1_user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        db.execute(
            'INSERT INTO teachers (id, name, gender, college, title, contact, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('T20250001', '李教授', 'M', '计算机学院', '教授', 'teacher1@school.edu.cn', teacher1_user_id)
        )
        
        db.execute(
            'INSERT INTO users (username, password, real_name, role_id, contact) VALUES (?, ?, ?, ?, ?)',
            ('t002', hash_password('teacher123'), '王副教授', 2, 'teacher2@school.edu.cn')
        )
        teacher2_user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        db.execute(
            'INSERT INTO teachers (id, name, gender, college, title, contact, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('T20250002', '王副教授', 'F', '计算机学院', '副教授', 'teacher2@school.edu.cn', teacher2_user_id)
        )
        
        # 添加班级
        db.execute(
            'INSERT INTO classes (name, major_id, grade_year, advisor_id) VALUES (?, ?, ?, ?)',
            ('计科2023级1班', 1, 2023, 'T20250001')
        )
        db.execute(
            'INSERT INTO classes (name, major_id, grade_year, advisor_id) VALUES (?, ?, ?, ?)',
            ('软工2023级1班', 2, 2023, 'T20250002')
        )
        
        # 添加学生用户和学生信息
        db.execute(
            'INSERT INTO users (username, password, real_name, role_id, contact) VALUES (?, ?, ?, ?, ?)',
            ('s001', hash_password('student123'), '张三', 3, 'student1@school.edu.cn')
        )
        student1_user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        db.execute(
            'INSERT INTO students (id, name, gender, birth_date, id_card, hometown, enrollment_date, major_id, class_id, phone, email, address, status, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            ('S20230001', '张三', 'M', '2005-01-15', '110101200501150011', '北京市', '2023-09-01', 1, 1, '13800138001', 'student1@school.edu.cn', '北京市海淀区', '在读', student1_user_id)
        )
        
        db.execute(
            'INSERT INTO users (username, password, real_name, role_id, contact) VALUES (?, ?, ?, ?, ?)',
            ('s002', hash_password('student123'), '李四', 3, 'student2@school.edu.cn')
        )
        student2_user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        db.execute(
            'INSERT INTO students (id, name, gender, birth_date, id_card, hometown, enrollment_date, major_id, class_id, phone, email, address, status, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            ('S20230002', '李四', 'F', '2005-05-20', '110101200505200022', '上海市', '2023-09-01', 2, 2, '13900139002', 'student2@school.edu.cn', '上海市静安区', '在读', student2_user_id)
        )
        
        # 添加课程
        db.execute(
            'INSERT INTO courses (code, name, course_type, credits, hours, college, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('CS101', '计算机导论', '必修', 3.0, 48, '计算机学院', '计算机科学基础课程，介绍计算机的基本概念和原理。')
        )
        
        db.execute(
            'INSERT INTO courses (code, name, course_type, credits, hours, college, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('CS102', '程序设计基础', '必修', 4.0, 64, '计算机学院', '介绍基本的程序设计方法和技巧，使用C++语言。')
        )
        
        db.execute(
            'INSERT INTO courses (code, name, course_type, credits, hours, college, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('MA101', '高等数学', '必修', 5.0, 80, '理学院', '微积分和线性代数的基础知识。')
        )
        
        # 添加开课信息
        db.execute(
            'INSERT INTO offered_courses (course_id, academic_year, semester, teacher_id, schedule, location, capacity, selected_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (1, '2024-2025', '第一学期', 'T20250001', '周一 1-2节', '教学楼A-101', 60, 2)
        )
        
        db.execute(
            'INSERT INTO offered_courses (course_id, academic_year, semester, teacher_id, schedule, location, capacity, selected_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (2, '2024-2025', '第一学期', 'T20250002', '周三 3-4节', '教学楼B-202', 50, 2)
        )
        
        db.execute(
            'INSERT INTO offered_courses (course_id, academic_year, semester, teacher_id, schedule, location, capacity, selected_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (3, '2024-2025', '第一学期', 'T20250001', '周五 5-6节', '教学楼C-303', 70, 2)
        )
        
        # 添加选课记录
        db.execute(
            'INSERT INTO course_selections (student_id, offered_course_id, selection_time, status) VALUES (?, ?, ?, ?)',
            ('S20230001', 1, '2024-06-01 10:00:00', '已选')
        )
        
        db.execute(
            'INSERT INTO course_selections (student_id, offered_course_id, selection_time, status) VALUES (?, ?, ?, ?)',
            ('S20230001', 2, '2024-06-01 10:30:00', '已选')
        )
        
        db.execute(
            'INSERT INTO course_selections (student_id, offered_course_id, selection_time, status) VALUES (?, ?, ?, ?)',
            ('S20230002', 1, '2024-06-02 14:00:00', '已选')
        )
        
        db.execute(
            'INSERT INTO course_selections (student_id, offered_course_id, selection_time, status) VALUES (?, ?, ?, ?)',
            ('S20230002', 3, '2024-06-02 14:30:00', '已选')
        )
        
        # 添加成绩
        db.execute(
            'INSERT INTO grades (student_id, offered_course_id, regular_grade, exam_grade, final_grade, gpa, input_time, input_teacher_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            ('S20230001', 1, 85.0, 90.0, 88.0, 4.0, '2025-01-10 15:00:00', 'T20250001', '已审核')
        )
        
        db.execute(
            'INSERT INTO grades (student_id, offered_course_id, regular_grade, exam_grade, final_grade, gpa, input_time, input_teacher_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            ('S20230001', 2, 80.0, 85.0, 83.0, 3.5, '2025-01-11 10:00:00', 'T20250002', '已审核')
        )
        
        # 添加学费信息
        db.execute(
            'INSERT INTO tuitions (student_id, academic_year, amount, paid_amount, status, deadline) VALUES (?, ?, ?, ?, ?, ?)',
            ('S20230001', '2024-2025', 8000.0, 0.0, '未缴费', '2024-09-15')
        )
        
        db.execute(
            'INSERT INTO tuitions (student_id, academic_year, amount, paid_amount, status, deadline) VALUES (?, ?, ?, ?, ?, ?)',
            ('S20230002', '2024-2025', 8000.0, 8000.0, '已缴费', '2024-09-15')
        )
        
        # 获取第二个学生的学费ID
        tuition2_id = db.execute('SELECT id FROM tuitions WHERE student_id = ?', ('S20230002',)).fetchone()[0]
        
        # 添加支付记录
        db.execute(
            'INSERT INTO payments (tuition_id, amount, payment_time, payment_method, transaction_id) VALUES (?, ?, ?, ?, ?)',
            (tuition2_id, 8000.0, '2024-08-20 11:00:00', '银行转账', 'P20240820001')
        )
        
        db.commit()
        
        print("数据库初始化完成，测试数据已添加！")

if __name__ == '__main__':
    init_db()
