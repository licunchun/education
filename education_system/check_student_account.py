from education_system import app, db
from education_system.models.database import Student, User
import hashlib

def check_student_account(student_id, password):
    with app.app_context():
        # 查找学生
        student = Student.query.filter_by(id=student_id).first()
        
        if student:
            print(f"找到学生: {student.name}, 学号: {student.id}")
            
            if student.user:
                print(f"关联的用户ID: {student.user.id}, 用户名: {student.user.username}")
                print(f"用户状态: {'启用' if student.user.status else '禁用'}")
                
                # 计算输入密码的哈希值
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                print(f"输入密码的哈希值: {hashed_password}")
                print(f"数据库中的密码哈希值: {student.user.password}")
                
                if student.user.password == hashed_password:
                    print("密码匹配成功!")
                else:
                    print("密码不匹配!")
            else:
                print("该学生没有关联的用户账户!")
        else:
            print(f"找不到学号为 {student_id} 的学生")
            
            # 检查用户表
            user = User.query.filter_by(username=student_id).first()
            if user:
                print(f"但是在用户表中找到了用户名为 {student_id} 的账户")
                print(f"用户ID: {user.id}, 真实姓名: {user.real_name}")
                
                # 计算输入密码的哈希值
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                print(f"输入密码的哈希值: {hashed_password}")
                print(f"数据库中的密码哈希值: {user.password}")
                
                if user.password == hashed_password:
                    print("密码匹配成功!")
                else:
                    print("密码不匹配!")
            else:
                print(f"在用户表中也找不到用户名为 {student_id} 的账户")
        
        # 检查是否有其他相似的学号
        similar_students = Student.query.filter(Student.id.like(f"%{student_id[-4:]}%")).all()
        if similar_students and len(similar_students) > 0:
            print("\n找到可能相似的学号:")
            for s in similar_students:
                print(f"学号: {s.id}, 姓名: {s.name}")

if __name__ == "__main__":
    check_student_account("20051008", "123456")
