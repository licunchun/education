#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：为学生表添加account_balance字段
执行此脚本将为所有现有学生初始化账户余额为0
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from education_system import db, app
from education_system.models.database import Student

def add_balance_field():
    """为学生表添加account_balance字段并初始化"""
    with app.app_context():
        try:
            from sqlalchemy import text
            
            # 检查是否已经有account_balance字段（MySQL语法）
            with db.engine.connect() as connection:
                result = connection.execute(text("SHOW COLUMNS FROM students LIKE 'account_balance'"))
                columns = list(result)
                
                if not columns:
                    print("添加account_balance字段...")
                    # 添加字段（MySQL语法）
                    connection.execute(text("ALTER TABLE students ADD COLUMN account_balance FLOAT DEFAULT 0.0"))
                    connection.commit()
                    print("✓ account_balance字段添加成功")
                else:
                    print("account_balance字段已存在")
            
            # 更新所有现有学生的余额为0（如果是NULL的话）
            students = Student.query.filter(Student.account_balance.is_(None)).all()
            if students:
                print(f"初始化 {len(students)} 个学生的账户余额...")
                for student in students:
                    student.account_balance = 0.0
                db.session.commit()
                print("✓ 学生账户余额初始化完成")
            else:
                print("所有学生账户余额已初始化")
            
            # 验证结果
            total_students = Student.query.count()
            zero_balance_students = Student.query.filter_by(account_balance=0.0).count()
            print(f"\n数据统计:")
            print(f"总学生数: {total_students}")
            print(f"余额为0的学生数: {zero_balance_students}")
            print(f"其他余额学生数: {total_students - zero_balance_students}")
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    print("开始数据库迁移：添加学生账户余额字段")
    print("=" * 50)
    
    if add_balance_field():
        print("\n✅ 数据库迁移完成！")
        print("所有学生的账户余额已初始化为0.0")
    else:
        print("\n❌ 数据库迁移失败！")
        sys.exit(1)
