from education_system import app, db
from education_system.models.database import RegistrationApplication
from sqlalchemy import text
import sys

def add_credential_fields():
    try:
        print("正在添加学号/教师号和初始密码字段...")
        with app.app_context():
            # 使用text对象和connection来执行SQL
            with db.engine.connect() as conn:
                conn.execute(text('''
                    ALTER TABLE registration_applications 
                    ADD COLUMN assigned_id VARCHAR(50),
                    ADD COLUMN initial_password VARCHAR(50)
                '''))
                conn.commit()
            print("字段添加成功！")
            return True
    except Exception as e:
        print(f"添加字段时出错：{str(e)}")
        return False
        
if __name__ == "__main__":
    success = add_credential_fields()
    sys.exit(0 if success else 1)
