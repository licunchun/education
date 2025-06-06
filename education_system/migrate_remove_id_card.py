#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的数据库迁移脚本：删除身份证号字段
"""

import sqlite3
import os
import shutil
from datetime import datetime

def migrate_database():
    db_path = "education.db"
    
    # 备份数据库
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(db_path, backup_path)
    print(f"数据库已备份至: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 删除学生表的id_card字段
        print("处理学生表...")
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
                user_id INTEGER UNIQUE
            )
        ''')
        
        cursor.execute('''
            INSERT INTO students_new 
            SELECT id, name, gender, birth_date, hometown, enrollment_date, 
                   major_id, class_id, phone, email, address, photo_path, 
                   status, user_id 
            FROM students
        ''')
        
        cursor.execute('DROP TABLE students')
        cursor.execute('ALTER TABLE students_new RENAME TO students')
        
        # 删除申请表的id_number字段
        print("处理申请表...")
        cursor.execute('''
            CREATE TABLE registration_applications_new (
                id INTEGER PRIMARY KEY,
                application_type TEXT NOT NULL,
                name TEXT NOT NULL,
                gender TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                emergency_contact TEXT,
                emergency_phone TEXT,
                major_id INTEGER,
                class_id INTEGER,
                high_school TEXT,
                exam_score TEXT,
                guardian_name TEXT,
                guardian_phone TEXT,
                education_level TEXT,
                graduate_school TEXT,
                major_field TEXT,
                title TEXT,
                department TEXT,
                work_experience TEXT,
                specialties TEXT,
                special_notes TEXT,
                status TEXT DEFAULT '待审核',
                application_time TIMESTAMP,
                review_time TIMESTAMP,
                reviewer_id TEXT,
                review_comments TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO registration_applications_new 
            SELECT id, application_type, name, gender, phone, email, 
                   address, emergency_contact, emergency_phone, major_id, class_id, 
                   high_school, exam_score, guardian_name, guardian_phone, 
                   education_level, graduate_school, major_field, title, department, 
                   work_experience, specialties, special_notes, status, 
                   application_time, review_time, reviewer_id, review_comments
            FROM registration_applications
        ''')
        
        cursor.execute('DROP TABLE registration_applications')
        cursor.execute('ALTER TABLE registration_applications_new RENAME TO registration_applications')
        
        conn.commit()
        print("数据库迁移完成！身份证号字段已删除。")
        
    except Exception as e:
        conn.rollback()
        print(f"迁移失败: {e}")
        # 恢复备份
        shutil.copy2(backup_path, db_path)
        print("已恢复数据库备份")
        
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
