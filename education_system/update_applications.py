from education_system import app, db
from sqlalchemy import text

def update_applications():
    with app.app_context():
        try:
            # 直接使用SQL更新数据库中的申请记录
            print("开始更新申请记录...")
            
            # 查询当前的申请记录
            with db.engine.connect() as conn:
                # 查询已通过的申请
                result = conn.execute(text("""
                    SELECT id, name, application_type, status, assigned_id, initial_password, phone 
                    FROM registration_applications 
                    WHERE status = '已通过'
                """))
                print("\n当前已通过的申请:")
                
                student_exists = False
                teacher_exists = False
                
                for row in result:
                    app_id, name, app_type, status, assigned_id, initial_password, phone = row
                    print(f"  ID: {app_id}, 姓名: {name}, 类型: {app_type}, 状态: {status}")
                    print(f"  分配的ID: {assigned_id or '未设置'}, 初始密码: {initial_password or '未设置'}")
                    print(f"  手机号: {phone}")
                    print()
                    
                    if app_type == 'student':
                        student_exists = True
                    elif app_type == 'teacher':
                        teacher_exists = True
                
                # 更新所有已通过的教师申请，确保有assigned_id和initial_password
                result = conn.execute(text("""
                    UPDATE registration_applications 
                    SET assigned_id = CONCAT('T2025', LPAD(id, 3, '0')),
                        initial_password = '123456'
                    WHERE status = '已通过' 
                    AND application_type = 'teacher'
                """))
                conn.commit()
                
                # 更新所有已通过的学生申请，确保有assigned_id和initial_password
                result = conn.execute(text("""
                    UPDATE registration_applications 
                    SET assigned_id = CONCAT('2025', LPAD(id, 4, '0')),
                        initial_password = '123456'
                    WHERE status = '已通过' 
                    AND application_type = 'student'
                """))
                conn.commit()
                
                # 如果没有教师申请，创建一个
                if not teacher_exists:
                    print("没有找到教师申请，创建一个测试记录...")
                    conn.execute(text("""
                        INSERT INTO registration_applications 
                        (application_type, name, gender, phone, email, major_field, title, department, status, review_time, review_comments, assigned_id, initial_password) 
                        VALUES 
                        ('teacher', '测试教师', 'F', '13900139001', 'test_teacher@example.com', '计算机科学', '副教授', '计算机科学与技术学院', '已通过', NOW(), '测试通过', 'T2025001', '123456')
                    """))
                    conn.commit()
                    print("教师测试申请创建成功！")
                
                # 如果没有学生申请，创建一个
                if not student_exists:
                    print("没有找到学生申请，创建一个测试记录...")
                    conn.execute(text("""
                        INSERT INTO registration_applications 
                        (application_type, name, gender, phone, email, hometown, status, review_time, review_comments, assigned_id, initial_password) 
                        VALUES 
                        ('student', '测试学生', 'M', '13800138001', 'test_student@example.com', '北京', '已通过', NOW(), '测试通过', '20250001', '123456')
                    """))
                    conn.commit()
                    print("学生测试申请创建成功！")
                
                # 再次查询更新后的申请记录
                result = conn.execute(text("""
                    SELECT id, name, application_type, status, assigned_id, initial_password, phone 
                    FROM registration_applications 
                    WHERE status = '已通过'
                """))
                print("\n更新后的申请记录:")
                for row in result:
                    app_id, name, app_type, status, assigned_id, initial_password, phone = row
                    print(f"  ID: {app_id}, 姓名: {name}, 类型: {app_type}, 状态: {status}")
                    print(f"  分配的ID: {assigned_id or '未设置'}, 初始密码: {initial_password or '未设置'}")
                    print(f"  手机号: {phone}")
                    print()
                
                print("\n请使用以上手机号码在申请状态查询页面查看账号信息。")
            
        except Exception as e:
            print(f"更新申请记录失败: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    update_applications()
