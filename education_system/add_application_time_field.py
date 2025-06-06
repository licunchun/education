from education_system import app, db
from education_system.models.database import RegistrationApplication
from sqlalchemy import text
import sys

def add_application_time_field():
    try:
        print("开始执行迁移脚本...")
        print("正在检查并添加application_time字段...")
        with app.app_context():
            # 检查字段是否已存在
            with db.engine.connect() as conn:
                print("数据库连接成功，检查字段是否存在...")
                result = conn.execute(text('''
                    SELECT COUNT(*) 
                    FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'registration_applications' 
                    AND COLUMN_NAME = 'application_time'
                '''))
                count = result.scalar()
                print(f"检查结果: application_time字段存在计数 = {count}")
                
                if count == 0:
                    # 字段不存在，添加它
                    print("字段不存在，正在添加...")
                    conn.execute(text('''
                        ALTER TABLE registration_applications 
                        ADD COLUMN application_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    '''))
                    conn.commit()
                    print("application_time字段添加成功！")
                else:
                    print("application_time字段已经存在，无需添加。")
                
            return True
    except Exception as e:
        print(f"添加字段时出错：{str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
if __name__ == "__main__":
    print("脚本开始执行...")
    success = add_application_time_field()
    print(f"脚本执行结果: {'成功' if success else '失败'}")
    sys.exit(0 if success else 1)
