#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL数据库迁移脚本 - 删除班级ID相关字段
"""
import pymysql
import os
from datetime import datetime

def get_mysql_connection():
    """获取MySQL数据库连接"""
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', '3306')),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', '87893986lcc'),
        database=os.environ.get('DB_NAME', 'education_system'),
        charset='utf8mb4'
    )

def migrate_remove_class_fields():
    """移除班级ID相关字段"""
    print("🔧 开始MySQL数据库迁移：删除班级ID字段...")
    
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        
        # 备份数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        print("📋 正在备份表数据...")
        
        try:
            cursor.execute(f"CREATE TABLE students_backup_{timestamp} AS SELECT * FROM students")
            cursor.execute(f"CREATE TABLE registration_applications_backup_{timestamp} AS SELECT * FROM registration_applications")
            print(f"✅ 备份完成: students_backup_{timestamp}, registration_applications_backup_{timestamp}")
        except Exception as e:
            print(f"⚠️  备份失败: {e}")
        
        print("🗂️  开始删除字段...")
        
        # 1. 删除students表的外键约束和字段
        print("🔗 处理students表...")
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = 'education_system' 
            AND TABLE_NAME = 'students' 
            AND COLUMN_NAME = 'class_id'
        """)
        
        foreign_keys = cursor.fetchall()
        for fk in foreign_keys:
            fk_name = fk[0]
            try:
                cursor.execute(f"ALTER TABLE students DROP FOREIGN KEY {fk_name}")
                print(f"✅ 已删除外键约束: {fk_name}")
            except Exception as e:
                print(f"⚠️  删除外键约束失败: {e}")
        
        # 删除students表的class_id字段
        cursor.execute("SHOW COLUMNS FROM students LIKE 'class_id'")
        if cursor.fetchone():
            try:
                cursor.execute("ALTER TABLE students DROP COLUMN class_id")
                print("✅ 已删除students表中的class_id字段")
            except Exception as e:
                print(f"⚠️  删除students.class_id字段失败: {e}")
        else:
            print("ℹ️  students表中没有class_id字段")
        
        # 2. 删除registration_applications表的外键约束和字段
        print("🔗 处理registration_applications表...")
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = 'education_system' 
            AND TABLE_NAME = 'registration_applications' 
            AND COLUMN_NAME = 'class_id'
        """)
        
        app_foreign_keys = cursor.fetchall()
        for fk in app_foreign_keys:
            fk_name = fk[0]
            try:
                cursor.execute(f"ALTER TABLE registration_applications DROP FOREIGN KEY {fk_name}")
                print(f"✅ 已删除外键约束: {fk_name}")
            except Exception as e:
                print(f"⚠️  删除外键约束失败: {e}")
        
        # 删除registration_applications表的class_id字段
        cursor.execute("SHOW COLUMNS FROM registration_applications LIKE 'class_id'")
        if cursor.fetchone():
            try:
                cursor.execute("ALTER TABLE registration_applications DROP COLUMN class_id")
                print("✅ 已删除registration_applications表中的class_id字段")
            except Exception as e:
                print(f"⚠️  删除registration_applications.class_id字段失败: {e}")
        else:
            print("ℹ️  registration_applications表中没有class_id字段")
        
        connection.commit()
        print("✅ 数据库迁移完成！")
        
        # 验证迁移结果
        print("\n📊 验证迁移结果:")
        cursor.execute("SHOW COLUMNS FROM students")
        student_columns = [col[0] for col in cursor.fetchall()]
        print(f"students表字段: {', '.join(student_columns)}")
        
        cursor.execute("SHOW COLUMNS FROM registration_applications")  
        app_columns = [col[0] for col in cursor.fetchall()]
        print(f"registration_applications表字段: {', '.join(app_columns)}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()

def verify_migration():
    """验证迁移结果"""
    print("\n🔍 验证数据完整性...")
    
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        
        # 检查学生数据
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        print(f"✅ students表记录数: {student_count}")
        
        # 检查申请数据
        cursor.execute("SELECT COUNT(*) FROM registration_applications")
        app_count = cursor.fetchone()[0]
        print(f"✅ registration_applications表记录数: {app_count}")
        
        # 检查是否还有class_id字段
        cursor.execute("SHOW COLUMNS FROM students")
        student_columns = [col[0] for col in cursor.fetchall()]
        has_class_id_students = 'class_id' in student_columns
        
        cursor.execute("SHOW COLUMNS FROM registration_applications")
        app_columns = [col[0] for col in cursor.fetchall()]
        has_class_id_apps = 'class_id' in app_columns
        
        if not has_class_id_students and not has_class_id_apps:
            print("✅ 班级ID字段已成功删除")
        else:
            print("⚠️  仍有班级ID字段残留")
            if has_class_id_students:
                print("   - students表仍有class_id字段")
            if has_class_id_apps:
                print("   - registration_applications表仍有class_id字段")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")

if __name__ == '__main__':
    print("🎓 MySQL数据库迁移工具")
    print("=" * 50)
    
    # 执行迁移
    migrate_remove_class_fields()
    
    # 验证结果
    verify_migration()
    
    print("\n✅ 迁移完成！")
    print("💡 如有问题，可以使用备份表恢复数据")
