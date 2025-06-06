from education_system import app, db
from sqlalchemy import text

def check_applications_raw():
    with app.app_context():
        try:
            # 使用原始SQL查询检查表结构
            with db.engine.connect() as conn:
                # 检查表结构
                result = conn.execute(text("DESCRIBE registration_applications"))
                print("表结构:")
                for row in result:
                    print(f"  {row[0]} - {row[1]}")
                
                # 查询已通过的申请
                result = conn.execute(text("SELECT id, name, application_type, status, assigned_id, initial_password FROM registration_applications WHERE status = '已通过'"))
                print("\n已通过的申请:")
                for row in result:
                    print(f"  ID: {row[0]}, 姓名: {row[1]}, 类型: {row[2]}, 状态: {row[3]}")
                    print(f"  分配的ID: {row[4] or '未设置'}, 初始密码: {row[5] or '未设置'}")
                    print()
                
                # 更新缺少账号信息的已通过申请
                result = conn.execute(text("""
                    UPDATE registration_applications 
                    SET assigned_id = CONCAT('T2025', LPAD(id, 3, '0')),
                        initial_password = '123456'
                    WHERE status = '已通过' 
                    AND (assigned_id IS NULL OR assigned_id = '')
                    AND application_type = 'teacher'
                """))
                conn.commit()
                
                result = conn.execute(text("""
                    UPDATE registration_applications 
                    SET assigned_id = CONCAT('2025', LPAD(id, 4, '0')),
                        initial_password = '123456'
                    WHERE status = '已通过' 
                    AND (assigned_id IS NULL OR assigned_id = '')
                    AND application_type = 'student'
                """))
                conn.commit()
                
                # 再次查询已通过的申请
                result = conn.execute(text("SELECT id, name, application_type, status, assigned_id, initial_password FROM registration_applications WHERE status = '已通过'"))
                print("\n更新后的已通过申请:")
                for row in result:
                    print(f"  ID: {row[0]}, 姓名: {row[1]}, 类型: {row[2]}, 状态: {row[3]}")
                    print(f"  分配的ID: {row[4] or '未设置'}, 初始密码: {row[5] or '未设置'}")
                    print()
                
        except Exception as e:
            print(f"检查申请记录时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    check_applications_raw()
