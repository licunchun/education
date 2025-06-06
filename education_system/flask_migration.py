#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Flask应用上下文执行MySQL迁移
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from education_system import app, db
from sqlalchemy import text

def migrate_remove_class_fields():
    """删除班级ID字段"""
    print("🔧 开始删除班级ID字段...")
    
    with app.app_context():
        try:
            # 检查students表中的外键约束
            print("🔗 检查students表外键约束...")
            result = db.session.execute(text("""
                SELECT CONSTRAINT_NAME 
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE TABLE_SCHEMA = 'education_system' 
                AND TABLE_NAME = 'students' 
                AND COLUMN_NAME = 'class_id'
            """))
            
            foreign_keys = result.fetchall()
            for fk in foreign_keys:
                fk_name = fk[0]
                try:
                    db.session.execute(text(f"ALTER TABLE students DROP FOREIGN KEY {fk_name}"))
                    print(f"✅ 删除外键约束: {fk_name}")
                except Exception as e:
                    print(f"⚠️  删除外键失败: {e}")
            
            # 删除students表的class_id字段
            print("🗂️  删除students表的class_id字段...")
            try:
                # 先检查字段是否存在
                result = db.session.execute(text("SHOW COLUMNS FROM students LIKE 'class_id'"))
                if result.fetchone():
                    db.session.execute(text("ALTER TABLE students DROP COLUMN class_id"))
                    print("✅ 删除students.class_id字段成功")
                else:
                    print("ℹ️  students表中没有class_id字段")
            except Exception as e:
                print(f"⚠️  删除students.class_id字段失败: {e}")
            
            # 检查registration_applications表中的外键约束
            print("🔗 检查registration_applications表外键约束...")
            result = db.session.execute(text("""
                SELECT CONSTRAINT_NAME 
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE TABLE_SCHEMA = 'education_system' 
                AND TABLE_NAME = 'registration_applications' 
                AND COLUMN_NAME = 'class_id'
            """))
            
            app_foreign_keys = result.fetchall()
            for fk in app_foreign_keys:
                fk_name = fk[0]
                try:
                    db.session.execute(text(f"ALTER TABLE registration_applications DROP FOREIGN KEY {fk_name}"))
                    print(f"✅ 删除外键约束: {fk_name}")
                except Exception as e:
                    print(f"⚠️  删除外键失败: {e}")
            
            # 删除registration_applications表的class_id字段
            print("🗂️  删除registration_applications表的class_id字段...")
            try:
                # 先检查字段是否存在
                result = db.session.execute(text("SHOW COLUMNS FROM registration_applications LIKE 'class_id'"))
                if result.fetchone():
                    db.session.execute(text("ALTER TABLE registration_applications DROP COLUMN class_id"))
                    print("✅ 删除registration_applications.class_id字段成功")
                else:
                    print("ℹ️  registration_applications表中没有class_id字段")
            except Exception as e:
                print(f"⚠️  删除registration_applications.class_id字段失败: {e}")
            
            # 提交更改
            db.session.commit()
            print("✅ 数据库迁移完成！")
            
            # 验证结果
            print("\n📊 验证迁移结果:")
            result = db.session.execute(text("SHOW COLUMNS FROM students"))
            student_columns = [col[0] for col in result.fetchall()]
            print(f"students表字段: {', '.join(student_columns)}")
            
            result = db.session.execute(text("SHOW COLUMNS FROM registration_applications"))
            app_columns = [col[0] for col in result.fetchall()]
            print(f"registration_applications表字段: {', '.join(app_columns)}")
            
            has_class_id = 'class_id' in student_columns or 'class_id' in app_columns
            if not has_class_id:
                print("\n✅ 班级ID字段删除成功!")
            else:
                print("\n⚠️  仍有班级ID字段残留")
            
        except Exception as e:
            print(f"❌ 迁移失败: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("🎓 MySQL数据库迁移工具 (Flask版)")
    print("=" * 50)
    migrate_remove_class_fields()
