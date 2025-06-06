from education_system import app, db
from education_system.models.database import Student, User, RegistrationApplication
import hashlib

def list_all_students():
    with app.app_context():
        students = Student.query.all()
        print(f"总共找到 {len(students)} 个学生记录:")
        for student in students:
            print(f"学号: {student.id}, 姓名: {student.name}")
            if hasattr(student, 'user') and student.user:
                print(f"  关联用户: {student.user.username}, 状态: {'启用' if student.user.status else '禁用'}")
            else:
                print("  无关联用户")
        
        print("\n检查已通过的申请记录:")
        approved_apps = RegistrationApplication.query.filter_by(status='已通过').all()
        print(f"总共找到 {len(approved_apps)} 个已通过的申请记录:")
        for app in approved_apps:
            print(f"ID: {app.id}, 姓名: {app.name}, 类型: {app.application_type}")
            print(f"  分配ID: {app.assigned_id}, 初始密码: {app.initial_password}")

def check_specific_password(student_id, password):
    with app.app_context():
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        print(f"\n检查特定密码:")
        print(f"学号: {student_id}, 密码: {password}")
        print(f"密码哈希值: {hashed_password}")

if __name__ == "__main__":
    list_all_students()
    check_specific_password("20251008", "123456")
