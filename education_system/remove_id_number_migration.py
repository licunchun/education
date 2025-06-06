#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：删除身份证号字段
此脚本会从数据库中删除学生表和注册申请表中的身份证号字段
"""

import sqlite3
import os
import shutil
from datetime import datetime

def backup_database(db_path):
    """备份数据库"""
    if os.path.exists(db_path):
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(db_path, backup_path)
        print(f"数据库已备份至: {backup_path}")
        return backup_path
    else:
        print(f"数据库文件不存在: {db_path}")
        return None

def remove_id_number_fields(db_path):
    """删除身份证号字段"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查是否存在身份证号字段
        cursor.execute("PRAGMA table_info(students)")
        student_columns = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(registration_applications)")
        app_columns = [col[1] for col in cursor.fetchall()]
        
        print("当前学生表字段:", student_columns)
        print("当前申请表字段:", app_columns)
        
        # 如果学生表有身份证号字段，删除它
        if 'id_card' in student_columns:
            print("开始删除学生表中的身份证号字段...")
            
            # 创建临时表（不包含id_card字段）
            cursor.execute('''
                CREATE TABLE students_new (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    gender TEXT,
                    birth_date DATE,
                    hometown TEXT,
                    enrollment_date DATE,
                    major_id INTEGER,
                    class_id INTEGER,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    photo_path TEXT,
                    status TEXT DEFAULT '在读',
                    account_balance REAL DEFAULT 0.0,
                    user_id INTEGER UNIQUE,
                    FOREIGN KEY (major_id) REFERENCES majors (id),
                    FOREIGN KEY (class_id) REFERENCES classes (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
              # 复制数据（除了id_card字段）
            cursor.execute('''
                INSERT INTO students_new 
                SELECT id, name, gender, birth_date, hometown, enrollment_date, 
                       major_id, class_id, phone, email, address, photo_path, 
                       status, 0.0, user_id 
                FROM students
            ''')
            
            # 删除原表，重命名新表
            cursor.execute('DROP TABLE students')
            cursor.execute('ALTER TABLE students_new RENAME TO students')
            
            print("学生表身份证号字段删除完成")
        else:
            print("学生表中未找到身份证号字段")
        
        # 如果申请表有身份证号字段，删除它
        if 'id_number' in app_columns:
            print("开始删除申请表中的身份证号字段...")
            
            # 创建临时表（不包含id_number字段）
            cursor.execute('''
                CREATE TABLE registration_applications_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    gender TEXT,
                    phone TEXT,
                    email TEXT,
                    birth_date DATE,
                    hometown TEXT,
                    major_id INTEGER,
                    class_id INTEGER,
                    guardian_name TEXT,
                    guardian_phone TEXT,
                    address TEXT,
                    major_field TEXT,
                    title TEXT,
                    department TEXT,
                    work_experience TEXT,
                    specialties TEXT,
                    special_notes TEXT,
                    status TEXT DEFAULT '待审核',
                    application_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    review_time DATETIME,
                    reviewer_id TEXT,
                    review_comments TEXT,
                    FOREIGN KEY (major_id) REFERENCES majors (id),
                    FOREIGN KEY (class_id) REFERENCES classes (id)
                )
            ''')
              # 复制数据（除了id_number字段）
            cursor.execute('''
                INSERT INTO registration_applications_new 
                SELECT id, application_type, name, gender, phone, email, 
                       NULL, NULL, major_id, class_id, guardian_name, 
                       guardian_phone, address, major_field, title, department, 
                       work_experience, specialties, special_notes, status, 
                       application_time, review_time, reviewer_id, review_comments
                FROM registration_applications
            ''')
            
            # 删除原表，重命名新表
            cursor.execute('DROP TABLE registration_applications')
            cursor.execute('ALTER TABLE registration_applications_new RENAME TO registration_applications')
            
            print("申请表身份证号字段删除完成")
        else:
            print("申请表中未找到身份证号字段")
        
        conn.commit()
        print("数据库迁移完成！")
        
    except Exception as e:
        conn.rollback()
        print(f"迁移过程中出现错误: {e}")
        raise
    finally:
        conn.close()

def main():
    """主函数"""
    db_path = "education.db"
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        print("请确保在正确的目录运行此脚本")
        return
    
    print("=" * 50)
    print("数据库迁移：删除身份证号字段")
    print("=" * 50)
    
    # 备份数据库
    backup_path = backup_database(db_path)
    if not backup_path:
        return
    
    # 确认操作
    response = input("是否继续删除身份证号字段？(y/N): ")
    if response.lower() != 'y':
        print("操作已取消")
        return
    
    try:
        # 执行迁移
        remove_id_number_fields(db_path)
        print("\n迁移成功完成！")
        print(f"备份文件位置: {backup_path}")
    except Exception as e:
        print(f"\n迁移失败: {e}")
        print(f"可以从备份文件恢复: {backup_path}")

if __name__ == "__main__":
    main()
