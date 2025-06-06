from education_system import app, db
from sqlalchemy import text

def fix_database():
    with app.app_context():
        try:
            # 添加application_time字段
            with db.engine.connect() as conn:
                try:
                    conn.execute(text('ALTER TABLE registration_applications ADD COLUMN application_time DATETIME DEFAULT CURRENT_TIMESTAMP'))
                    conn.commit()
                    print("application_time字段添加成功")
                except Exception as e:
                    print(f"添加application_time字段时出错（可能已存在）: {str(e)}")
            
            # 确保assigned_id和initial_password字段存在
            with db.engine.connect() as conn:
                try:
                    conn.execute(text('ALTER TABLE registration_applications ADD COLUMN assigned_id VARCHAR(50)'))
                    conn.commit()
                    print("assigned_id字段添加成功")
                except Exception as e:
                    print(f"添加assigned_id字段时出错（可能已存在）: {str(e)}")
                
                try:
                    conn.execute(text('ALTER TABLE registration_applications ADD COLUMN initial_password VARCHAR(50)'))
                    conn.commit()
                    print("initial_password字段添加成功")
                except Exception as e:
                    print(f"添加initial_password字段时出错（可能已存在）: {str(e)}")
                    
            print("数据库修复完成！")
        except Exception as e:
            print(f"操作失败: {str(e)}")

if __name__ == "__main__":
    fix_database()
