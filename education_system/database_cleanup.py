#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的数据库清理脚本 - 删除班级ID和身份证号字段
"""
import pymysql
from datetime import datetime

def clean_database():
    """清理数据库中不需要的字段"""
    try:
        print("正在连接MySQL数据库...")
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='87893986lcc',
            database='education_system'
        )
        cursor = conn.cursor()
        print("✅ 数据库连接成功")
        
        # 1. 删除students表中的外键约束
        print("\n1. 检查并删除外键约束...")
        
        # 查询外键约束
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = 'education_system' 
            AND TABLE_NAME = 'students' 
            AND COLUMN_NAME = 'class_id'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        fk_constraints = cursor.fetchall()
        
        for constraint in fk_constraints:
            constraint_name = constraint[0]
            try:
                cursor.execute(f"ALTER TABLE students DROP FOREIGN KEY {constraint_name}")
                print(f"✅ 删除外键约束: {constraint_name}")
            except Exception as e:
                print(f"⚠️  删除外键约束失败: {e}")
        
        # 2. 删除registration_applications表中的外键约束
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = 'education_system' 
            AND TABLE_NAME = 'registration_applications' 
            AND COLUMN_NAME = 'class_id'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        fk_constraints = cursor.fetchall()
        
        for constraint in fk_constraints:
            constraint_name = constraint[0]
            try:
                cursor.execute(f"ALTER TABLE registration_applications DROP FOREIGN KEY {constraint_name}")
                print(f"✅ 删除外键约束: {constraint_name}")
            except Exception as e:
                print(f"⚠️  删除外键约束失败: {e}")
        
        # 3. 删除字段
        print("\n2. 删除字段...")
        
        # 删除students表的字段
        fields_to_remove = [
            ('students', 'class_id'),
            ('students', 'id_card'),
            ('registration_applications', 'class_id'),
            ('registration_applications', 'id_number')
        ]
        
        for table, field in fields_to_remove:
            try:
                # 检查字段是否存在
                cursor.execute(f"SHOW COLUMNS FROM {table} LIKE '{field}'")
                if cursor.fetchone():
                    cursor.execute(f"ALTER TABLE {table} DROP COLUMN {field}")
                    print(f"✅ 删除字段: {table}.{field}")
                else:
                    print(f"ℹ️  字段不存在: {table}.{field}")
            except Exception as e:
                print(f"⚠️  删除字段失败 {table}.{field}: {e}")
        
        # 4. 提交更改
        conn.commit()
        print("\n3. 验证删除结果...")
        
        # 验证students表
        cursor.execute("DESCRIBE students")
        student_columns = [row[0] for row in cursor.fetchall()]
        print(f"Students表字段: {', '.join(student_columns)}")
        
        # 验证registration_applications表
        cursor.execute("DESCRIBE registration_applications")
        app_columns = [row[0] for row in cursor.fetchall()]
        print(f"Registration_applications表字段: {', '.join(app_columns)}")
        
        # 检查是否还有不需要的字段
        unwanted_fields = []
        if 'class_id' in student_columns:
            unwanted_fields.append('students.class_id')
        if 'id_card' in student_columns:
            unwanted_fields.append('students.id_card')
        if 'class_id' in app_columns:
            unwanted_fields.append('registration_applications.class_id')
        if 'id_number' in app_columns:
            unwanted_fields.append('registration_applications.id_number')
        
        if unwanted_fields:
            print(f"⚠️  以下字段仍然存在: {', '.join(unwanted_fields)}")
        else:
            print("✅ 所有不需要的字段已成功删除！")
        
        cursor.close()
        conn.close()
        
        return len(unwanted_fields) == 0
        
    except Exception as e:
        print(f"❌ 数据库清理失败: {e}")
        return False

if __name__ == '__main__':
    print("=== 数据库字段清理工具 ===")
    success = clean_database()
    if success:
        print("\n🎉 数据库清理完成！现在可以启动应用了。")
    else:
        print("\n❌ 数据库清理未完全成功，请检查错误信息。")
