from education_system import app
from education_system.models.database import db, Role, User, Major, Class, Teacher, Student, Course, OfferedCourse, CourseSelection, Grade, Tuition, Payment
from datetime import datetime, date
import hashlib

def hash_password(password):
    """简单的密码哈希函数"""
    return hashlib.md5(password.encode()).hexdigest()

def init_db():
    """初始化数据库并添加测试数据"""
    with app.app_context():
        # 删除所有表
        db.drop_all()
        # 创建所有表
        db.create_all()
        
        # 添加角色
        role_admin = Role(name='admin', description='系统管理员')
        role_teacher = Role(name='teacher', description='教师')
        role_student = Role(name='student', description='学生')
        db.session.add_all([role_admin, role_teacher, role_student])
        db.session.commit()
        
        # 添加管理员用户
        admin_user = User(
            username='admin001',
            password=hash_password('admin123'),
            real_name='张管理',
            role_id=role_admin.id,
            contact='admin@school.edu.cn'
        )
        db.session.add(admin_user)
        db.session.commit()
        
        # 添加专业
        major_cs = Major(code='CS001', name='计算机科学与技术', college='计算机学院', duration=4)
        major_se = Major(code='SE001', name='软件工程', college='计算机学院', duration=4)
        major_math = Major(code='MA001', name='数学', college='理学院', duration=4)
        db.session.add_all([major_cs, major_se, major_math])
        db.session.commit()
        
        # 添加教师用户和教师信息
        teacher1_user = User(
            username='t001',
            password=hash_password('teacher123'),
            real_name='李教授',
            role_id=role_teacher.id,
            contact='teacher1@school.edu.cn'
        )
        db.session.add(teacher1_user)
        db.session.commit()
        
        teacher1 = Teacher(
            id='T20250001',
            name='李教授',
            gender='M',
            college='计算机学院',
            title='教授',
            contact='teacher1@school.edu.cn',
            user_id=teacher1_user.id
        )
        
        teacher2_user = User(
            username='t002',
            password=hash_password('teacher123'),
            real_name='王副教授',
            role_id=role_teacher.id,
            contact='teacher2@school.edu.cn'
        )
        db.session.add(teacher2_user)
        db.session.commit()
        
        teacher2 = Teacher(
            id='T20250002',
            name='王副教授',
            gender='F',
            college='计算机学院',
            title='副教授',
            contact='teacher2@school.edu.cn',
            user_id=teacher2_user.id
        )
        
        db.session.add_all([teacher1, teacher2])
        db.session.commit()
        
        # 添加班级
        class_cs1 = Class(name='计科2023级1班', major_id=major_cs.id, grade_year=2023, advisor_id=teacher1.id)
        class_se1 = Class(name='软工2023级1班', major_id=major_se.id, grade_year=2023, advisor_id=teacher2.id)
        db.session.add_all([class_cs1, class_se1])
        db.session.commit()
        
        # 添加学生用户和学生信息
        student1_user = User(
            username='s001',
            password=hash_password('student123'),
            real_name='张三',
            role_id=role_student.id,
            contact='student1@school.edu.cn'
        )
        db.session.add(student1_user)
        db.session.commit()
        
        student1 = Student(
            id='S20230001',
            name='张三',
            gender='M',
            birth_date=date(2005, 1, 15),
            id_card='110101200501150011',
            hometown='北京市',
            enrollment_date=date(2023, 9, 1),
            major_id=major_cs.id,
            class_id=class_cs1.id,
            phone='13800138001',
            email='student1@school.edu.cn',
            address='北京市海淀区',
            status='在读',
            user_id=student1_user.id
        )
        
        student2_user = User(
            username='s002',
            password=hash_password('student123'),
            real_name='李四',
            role_id=role_student.id,
            contact='student2@school.edu.cn'
        )
        db.session.add(student2_user)
        db.session.commit()
        
        student2 = Student(
            id='S20230002',
            name='李四',
            gender='F',
            birth_date=date(2005, 5, 20),
            id_card='110101200505200022',
            hometown='上海市',
            enrollment_date=date(2023, 9, 1),
            major_id=major_se.id,
            class_id=class_se1.id,
            phone='13900139002',
            email='student2@school.edu.cn',
            address='上海市静安区',
            status='在读',
            user_id=student2_user.id
        )
        
        db.session.add_all([student1, student2])
        db.session.commit()
        
        # 添加课程
        course1 = Course(
            code='CS101',
            name='计算机导论',
            course_type='必修',
            credits=3.0,
            hours=48,
            college='计算机学院',
            description='计算机科学基础课程，介绍计算机的基本概念和原理。'
        )
        
        course2 = Course(
            code='CS102',
            name='程序设计基础',
            course_type='必修',
            credits=4.0,
            hours=64,
            college='计算机学院',
            description='介绍基本的程序设计方法和技巧，使用C++语言。'
        )
        
        course3 = Course(
            code='MA101',
            name='高等数学',
            course_type='必修',
            credits=5.0,
            hours=80,
            college='理学院',
            description='微积分和线性代数的基础知识。'
        )
        
        db.session.add_all([course1, course2, course3])
        db.session.commit()
        
        # 添加开课信息
        offered_course1 = OfferedCourse(
            course_id=course1.id,
            academic_year='2024-2025',
            semester='第一学期',
            teacher_id=teacher1.id,
            schedule='周一 1-2节',
            location='教学楼A-101',
            capacity=60,
            selected_count=2
        )
        
        offered_course2 = OfferedCourse(
            course_id=course2.id,
            academic_year='2024-2025',
            semester='第一学期',
            teacher_id=teacher2.id,
            schedule='周三 3-4节',
            location='教学楼B-202',
            capacity=50,
            selected_count=2
        )
        
        offered_course3 = OfferedCourse(
            course_id=course3.id,
            academic_year='2024-2025',
            semester='第一学期',
            teacher_id=teacher1.id,
            schedule='周五 5-6节',
            location='教学楼C-303',
            capacity=70,
            selected_count=2
        )
        
        db.session.add_all([offered_course1, offered_course2, offered_course3])
        db.session.commit()
        
        # 添加选课记录
        selection1 = CourseSelection(
            student_id=student1.id,
            offered_course_id=offered_course1.id,
            selection_time=datetime(2024, 6, 1, 10, 0, 0),
            status='已选'
        )
        
        selection2 = CourseSelection(
            student_id=student1.id,
            offered_course_id=offered_course2.id,
            selection_time=datetime(2024, 6, 1, 10, 30, 0),
            status='已选'
        )
        
        selection3 = CourseSelection(
            student_id=student2.id,
            offered_course_id=offered_course1.id,
            selection_time=datetime(2024, 6, 2, 14, 0, 0),
            status='已选'
        )
        
        selection4 = CourseSelection(
            student_id=student2.id,
            offered_course_id=offered_course3.id,
            selection_time=datetime(2024, 6, 2, 14, 30, 0),
            status='已选'
        )
        
        db.session.add_all([selection1, selection2, selection3, selection4])
        db.session.commit()
        
        # 添加成绩
        grade1 = Grade(
            student_id=student1.id,
            offered_course_id=offered_course1.id,
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
            offered_course_id=offered_course2.id,
            regular_grade=80.0,
            exam_grade=85.0,
            final_grade=83.0,
            gpa=3.5,
            input_time=datetime(2025, 1, 11, 10, 0, 0),
            input_teacher_id=teacher2.id,
            status='已审核'
        )
        
        db.session.add_all([grade1, grade2])
        db.session.commit()
        
        # 添加学费信息
        tuition1 = Tuition(
            student_id=student1.id,
            academic_year='2024-2025',
            amount=8000.0,
            paid_amount=0.0,
            status='未缴费',
            deadline=date(2024, 9, 15)
        )
        
        tuition2 = Tuition(
            student_id=student2.id,
            academic_year='2024-2025',
            amount=8000.0,
            paid_amount=8000.0,
            status='已缴费',
            deadline=date(2024, 9, 15)
        )
        
        db.session.add_all([tuition1, tuition2])
        db.session.commit()
        
        # 添加支付记录
        payment1 = Payment(
            tuition_id=tuition2.id,
            amount=8000.0,
            payment_time=datetime(2024, 8, 20, 11, 0, 0),
            payment_method='银行转账',
            transaction_id='P20240820001'
        )
        
        db.session.add(payment1)
        db.session.commit()
        
        print("数据库初始化完成，测试数据已添加！")

if __name__ == '__main__':
    init_db()
