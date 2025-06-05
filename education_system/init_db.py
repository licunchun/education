#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL数据库初始化模块
负责创建数据库表结构并插入基础测试数据
"""
import hashlib
from datetime import datetime, date
from education_system import app, db
from education_system.models.database import (
    Role, User, Major, Class, Student, Teacher, Course, 
    OfferedCourse, CourseSelection, Grade, Tuition, Payment,
    RegistrationApplication, ApplicationReview
)

def hash_password(password):
    """简单的密码哈希函数"""
    return hashlib.md5(password.encode()).hexdigest()

def init_db():
    """初始化MySQL数据库并添加测试数据"""
    print("🔧 开始初始化MySQL数据库...")
    
    with app.app_context():
        # 删除所有表然后重新创建
        db.drop_all()
        db.create_all()
        print("📋 MySQL数据库表结构创建成功")
        
        # 添加角色
        admin_role = Role(name='admin', description='系统管理员')
        teacher_role = Role(name='teacher', description='教师')
        student_role = Role(name='student', description='学生')
        
        db.session.add_all([admin_role, teacher_role, student_role])
        db.session.commit()
        
        # 添加管理员用户
        admin_user = User(
            username='admin001',
            password=hash_password('admin123'),
            real_name='张管理',
            role_id=admin_role.id,
            contact='admin@school.edu.cn'
        )
        db.session.add(admin_user)
        db.session.commit()
        
        # 添加专业
        cs_major = Major(code='CS001', name='计算机科学与技术', college='计算机学院', duration=4)
        se_major = Major(code='SE001', name='软件工程', college='计算机学院', duration=4)
        ma_major = Major(code='MA001', name='数学', college='理学院', duration=4)
        
        db.session.add_all([cs_major, se_major, ma_major])
        db.session.commit()
        
        # 添加教师用户和教师信息
        teacher1_user = User(
            username='t001',
            password=hash_password('teacher123'),
            real_name='李教授',
            role_id=teacher_role.id,
            contact='t001@school.edu.cn'
        )
        
        teacher2_user = User(
            username='t002',
            password=hash_password('teacher123'),
            real_name='王副教授',
            role_id=teacher_role.id,
            contact='t002@school.edu.cn'
        )
        
        db.session.add_all([teacher1_user, teacher2_user])
        db.session.commit()
        
        teacher1 = Teacher(
            id='T20250001',
            name='李教授',
            gender='M',
            college='计算机学院',
            title='教授',
            contact='t001@school.edu.cn',
            user_id=teacher1_user.id
        )
        
        teacher2 = Teacher(
            id='T20250002',
            name='王副教授',
            gender='F',
            college='计算机学院',
            title='副教授',
            contact='t002@school.edu.cn',
            user_id=teacher2_user.id
        )
        
        db.session.add_all([teacher1, teacher2])
        db.session.commit()
        
        # 添加班级
        class1 = Class(name='计科2023级1班', major_id=cs_major.id, grade_year=2023, advisor_id=teacher1.id)
        class2 = Class(name='软工2023级1班', major_id=se_major.id, grade_year=2023, advisor_id=teacher2.id)
        
        db.session.add_all([class1, class2])
        db.session.commit()
        
        # 添加学生用户和学生信息
        student1_user = User(
            username='s001',
            password=hash_password('student123'),
            real_name='张三',
            role_id=student_role.id,
            contact='s001@school.edu.cn'
        )
        
        student2_user = User(
            username='s002',
            password=hash_password('student123'),
            real_name='李四',
            role_id=student_role.id,
            contact='s002@school.edu.cn'
        )
        
        db.session.add_all([student1_user, student2_user])
        db.session.commit()
        
        student1 = Student(
            id='S20230001',
            name='张三',
            gender='M',
            birth_date=date(2005, 1, 15),
            id_card='110101200501150011',
            hometown='北京市',
            enrollment_date=date(2023, 9, 1),
            major_id=cs_major.id,
            class_id=class1.id,
            phone='13812345678',
            email='s001@school.edu.cn',
            address='北京市某区某街道',
            status='在读',
            user_id=student1_user.id
        )
        
        student2 = Student(
            id='S20230002',
            name='李四',
            gender='F',
            birth_date=date(2005, 5, 20),
            id_card='110101200505200022',
            hometown='上海市',
            enrollment_date=date(2023, 9, 1),
            major_id=se_major.id,
            class_id=class2.id,
            phone='13887654321',
            email='s002@school.edu.cn',
            address='上海市某区某街道',
            status='在读',
            user_id=student2_user.id
        )
        
        db.session.add_all([student1, student2])
        db.session.commit()
        
        # 添加课程
        course1 = Course(
            code='CS101',
            name='计算机基础',
            course_type='必修',
            credits=3.0,
            hours=48,
            college='计算机学院',
            description='计算机科学基础课程'
        )
        
        course2 = Course(
            code='CS102',
            name='程序设计',
            course_type='必修',
            credits=4.0,
            hours=64,
            college='计算机学院',
            description='程序设计基础'
        )
        
        course3 = Course(
            code='MA101',
            name='高等数学',
            course_type='必修',
            credits=5.0,
            hours=80,
            college='理学院',
            description='数学基础课程'
        )
        
        db.session.add_all([course1, course2, course3])
        db.session.commit()
        
        # 添加开课信息
        offered1 = OfferedCourse(
            course_id=course1.id,
            academic_year='2023-2024',
            semester='秋季学期',
            teacher_id=teacher1.id,
            schedule='周一1-2节',
            location='A101',
            capacity=50,
            selected_count=2
        )
        
        offered2 = OfferedCourse(
            course_id=course2.id,
            academic_year='2023-2024',
            semester='秋季学期',
            teacher_id=teacher2.id,
            schedule='周三3-4节',
            location='B201',
            capacity=40,
            selected_count=2
        )
        
        db.session.add_all([offered1, offered2])
        db.session.commit()
        
        # 添加选课记录
        selection1 = CourseSelection(
            student_id=student1.id,
            offered_course_id=offered1.id,
            selection_time=datetime(2024, 6, 1, 10, 0, 0),
            status='已选'
        )
        
        selection2 = CourseSelection(
            student_id=student1.id,
            offered_course_id=offered2.id,
            selection_time=datetime(2024, 6, 1, 10, 30, 0),
            status='已选'
        )
        
        selection3 = CourseSelection(
            student_id=student2.id,
            offered_course_id=offered1.id,
            selection_time=datetime(2024, 6, 2, 14, 0, 0),
            status='已选'
        )
        
        db.session.add_all([selection1, selection2, selection3])
        db.session.commit()
        
        # 添加成绩
        grade1 = Grade(
            student_id=student1.id,
            offered_course_id=offered1.id,
            regular_grade=85.0,
            exam_grade=90.0,
            final_grade=88.0,
            gpa=4.0,
            input_time=datetime(2025, 1, 10, 15, 0, 0),
            input_teacher_id=teacher1.id,
            status='已审核'
        )
        
        grade2 = Grade(
            student_id=student1.id,
            offered_course_id=offered2.id,
            regular_grade=80.0,
            exam_grade=85.0,
            final_grade=83.0,
            gpa=3.5,
            input_time=datetime(2025, 1, 11, 10, 0, 0),
            input_teacher_id=teacher2.id,            status='已审核'
        )
        
        db.session.add_all([grade1, grade2])
        db.session.commit()
        
        print("✅ 基础数据插入成功")
        print("📊 MySQL数据库初始化完成！")

if __name__ == '__main__':
    init_db()
