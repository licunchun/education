from education_system import app, db
from education_system.models.database import RegistrationApplication
from datetime import datetime
import random

def create_test_application():
    with app.app_context():
        try:
            # 检查是否已有已通过的申请
            existing_app = RegistrationApplication.query.filter_by(status='已通过').first()
            if existing_app:
                if existing_app.assigned_id and existing_app.initial_password:
                    print(f"已存在已通过的申请，ID: {existing_app.id}, 姓名: {existing_app.name}")
                    print(f"分配的ID: {existing_app.assigned_id}, 初始密码: {existing_app.initial_password}")
                    return
                else:
                    # 更新现有申请，添加账号信息
                    if existing_app.application_type == 'teacher':
                        existing_app.assigned_id = f"T{datetime.now().year}{random.randint(1, 999):03d}"
                    else:
                        existing_app.assigned_id = f"{datetime.now().year}{random.randint(1, 9999):04d}"
                    existing_app.initial_password = '123456'
                    db.session.commit()
                    print(f"已更新现有申请，ID: {existing_app.id}, 姓名: {existing_app.name}")
                    print(f"分配的ID: {existing_app.assigned_id}, 初始密码: {existing_app.initial_password}")
                    return
            
            # 创建新的测试申请并直接设置为已通过
            application_type = random.choice(['student', 'teacher'])
            
            # 根据类型设置不同的字段
            if application_type == 'teacher':
                app_data = {
                    'application_type': 'teacher',
                    'name': '测试教师',
                    'gender': 'M',
                    'phone': '13800138000',
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
            else:
                app_data = {
                    'application_type': 'student',
                    'name': '测试学生',
                    'gender': 'F',
                    'phone': '13900139000',
                    'email': 'test_student@example.com',
                    'hometown': '北京',
                    'status': '已通过',
                    'application_time': datetime.now(),
                    'review_time': datetime.now(),
                    'review_comments': '测试通过',
                    'assigned_id': f"{datetime.now().year}{random.randint(1, 9999):04d}",
                    'initial_password': '123456'
                }
            
            application = RegistrationApplication(**app_data)
            db.session.add(application)
            db.session.commit()
            
            print(f"已创建测试申请，ID: {application.id}, 姓名: {application.name}")
            print(f"分配的ID: {application.assigned_id}, 初始密码: {application.initial_password}")
            print(f"请使用手机号 {application.phone} 查询申请状态")
            
        except Exception as e:
            db.session.rollback()
            print(f"创建测试申请失败: {str(e)}")

if __name__ == "__main__":
    create_test_application()
