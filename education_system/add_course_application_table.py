#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加课程申请表迁移脚本
"""
import pymysql
from datetime import datetime

def migrate_add_course_application_table():
    """添加课程申请表"""
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
        
        # 检查课程申请表是否已存在
        cursor.execute("SHOW TABLES LIKE 'course_applications'")
        if cursor.fetchone():
            print("ℹ️  课程申请表已存在，无需创建")
            return True
        
        # 创建课程申请表
        print("正在创建课程申请表...")
        create_table_sql = """
        CREATE TABLE course_applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            teacher_id VARCHAR(20) NOT NULL,
            course_id INT NOT NULL,
            academic_year VARCHAR(20) NOT NULL,
            semester VARCHAR(20) NOT NULL,
            schedule VARCHAR(100),
            location VARCHAR(100),
            capacity INT DEFAULT 60,
            application_note TEXT,
            application_time DATETIME,
            status VARCHAR(20) DEFAULT '待审核',
            review_time DATETIME,
            reviewer_id VARCHAR(50),
            review_comments TEXT,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (reviewer_id) REFERENCES users(username)
        )
        """
        cursor.execute(create_table_sql)
        
        # 提交更改
        conn.commit()
        print("✅ 课程申请表创建成功")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False

if __name__ == '__main__':
    print("=== 添加课程申请表迁移工具 ===")
    success = migrate_add_course_application_table()
    if success:
        print("\n🎉 迁移完成！现在可以使用课程申请功能了。")
    else:
        print("\n❌ 迁移未成功，请检查错误信息。")
