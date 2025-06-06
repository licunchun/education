from education_system import app
from sqlalchemy import text
import hashlib

def direct_query_database():
    # 启用SQL查询日志
    app.config['SQLALCHEMY_ECHO'] = True
    
    with app.app_context():
        try:
            # 使用原始SQL查询检查学生表
            with app.db.engine.connect() as conn:
                # 检查学生表
                result = conn.execute(text("SELECT * FROM students"))
                rows = result.fetchall()
                print(f"学生表中有 {len(rows)} 条记录")
                
                if rows:
                    for row in rows:
                        print(f"学号: {row[0]}, 姓名: {row[1]}")
                else:
                    print("学生表中没有记录")
                
                # 检查用户表
                result = conn.execute(text("SELECT * FROM users"))
                rows = result.fetchall()
                print(f"\n用户表中有 {len(rows)} 条记录")
                
                if rows:
                    for row in rows:
                        print(f"用户ID: {row[0]}, 用户名: {row[1]}, 真实姓名: {row[3]}")
                else:
                    print("用户表中没有记录")
                
                # 检查申请表中已通过的记录
                result = conn.execute(text("SELECT * FROM registration_applications WHERE status = '已通过'"))
                rows = result.fetchall()
                print(f"\n已通过的申请有 {len(rows)} 条记录")
                
                if rows:
                    for row in rows:
                        print(f"ID: {row[0]}, 姓名: {row[2]}, 类型: {row[1]}")
                        # 查找assigned_id列的索引
                        column_names = result.keys()
                        if 'assigned_id' in column_names:
                            assigned_id_index = column_names.index('assigned_id')
                            print(f"  分配ID: {row[assigned_id_index]}")
                        else:
                            print("  表中没有assigned_id列")
                        
                        if 'initial_password' in column_names:
                            initial_password_index = column_names.index('initial_password')
                            print(f"  初始密码: {row[initial_password_index]}")
                        else:
                            print("  表中没有initial_password列")
                else:
                    print("没有已通过的申请记录")
                
                # 检查指定学号的密码哈希
                password = "123456"
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                print(f"\n密码 '{password}' 的哈希值: {hashed_password}")
                
        except Exception as e:
            print(f"查询数据库时出错: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    direct_query_database()
