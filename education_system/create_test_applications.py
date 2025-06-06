from education_system import app, db
from education_system.models.database import RegistrationApplication
from datetime import datetime
import random

def create_test_applications():
    with app.app_context():
        try:
            # 检查是否已有已通过的学生申请
            student_app = RegistrationApplication.query.filter_by(
                status='已通过', 
                application_type='student'
            ).first()
            
            if student_app:
                if not student_app.assigned_id or not student_app.initial_password:
                    # 更新现有学生申请，添加账号信息
                    student_app.assigned_id = f"{datetime.now().year}{random.randint(1, 9999):04d}"
                    student_app.initial_password = '123456'
                    db.session.commit()
                print(f"已存在已通过的学生申请，ID: {student_app.id}, 姓名: {student_app.name}")
                print(f"学生学号: {student_app.assigned_id}, 初始密码: {student_app.initial_password}")
            else:
                # 创建新的学生测试申请
                student_data = {
                    'application_type': 'student',
                    'name': '测试学生',
                    'gender': 'M',
                    'phone': '13800138001',
                    'email': 'test_student@example.com',
                    'hometown': '北京',
                    'status': '已通过',
                    'application_time': datetime.now(),
                    'review_time': datetime.now(),
                    'review_comments': '测试通过',
                    'assigned_id': f"{datetime.now().year}{random.randint(1, 9999):04d}",
                    'initial_password': '123456'
                }
                student_app = RegistrationApplication(**student_data)
                db.session.add(student_app)
                db.session.commit()
                print(f"已创建学生测试申请，ID: {student_app.id}, 姓名: {student_app.name}")
                print(f"学生学号: {student_app.assigned_id}, 初始密码: {student_app.initial_password}")
            
            # 检查是否已有已通过的教师申请
            teacher_app = RegistrationApplication.query.filter_by(
                status='已通过', 
                application_type='teacher'
            ).first()
            
            if teacher_app:
                if not teacher_app.assigned_id or not teacher_app.initial_password:
                    # 更新现有教师申请，添加账号信息
                    teacher_app.assigned_id = f"T{datetime.now().year}{random.randint(1, 999):03d}"
                    teacher_app.initial_password = '123456'
                    db.session.commit()
                print(f"已存在已通过的教师申请，ID: {teacher_app.id}, 姓名: {teacher_app.name}")
                print(f"教师工号: {teacher_app.assigned_id}, 初始密码: {teacher_app.initial_password}")
            else:
                # 创建新的教师测试申请
                teacher_data = {
                    'application_type': 'teacher',
                    'name': '测试教师',
                    'gender': 'F',
                    'phone': '13900139001',
                    'email': 'test_teacher@example.com',
                    'major_field': '计算机科学',
                    'title': '副教授',
                    'department': '计算机科学与技术学院',
                    'status': '已通过',
                    'application_time': datetime.now(),
                    'review_time': datetime.now(),
                    'review_comments': '测试通过',
                    'assigned_id': f"T{datetime.now().year}{random.randint(1, 999):03d}",
                    'initial_password': '123456'
                }
                teacher_app = RegistrationApplication(**teacher_data)
                db.session.add(teacher_app)
                db.session.commit()
                print(f"已创建教师测试申请，ID: {teacher_app.id}, 姓名: {teacher_app.name}")
                print(f"教师工号: {teacher_app.assigned_id}, 初始密码: {teacher_app.initial_password}")
                
            print("\n请使用以下信息查询申请状态：")
            print(f"学生申请 - 手机号: {student_app.phone}")
            print(f"教师申请 - 手机号: {teacher_app.phone}")
            
        except Exception as e:
            db.session.rollback()
            print(f"创建测试申请失败: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_test_applications()
