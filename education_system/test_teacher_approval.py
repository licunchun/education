#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试教师申请审批功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy

# 配置MySQL数据库连接
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL数据库配置
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'education_system'
DB_USER = 'root'
DB_PASSWORD = '87893986lcc'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {'charset': 'utf8mb4'}
}

# 初始化SQLAlchemy
db = SQLAlchemy(app)

# 导入模型
from models.database import *

def test_teacher_id_generation():
    """测试教师工号生成功能"""
    from routes import _generate_teacher_id
    
    with app.app_context():
        print("=== 测试教师工号生成 ===")
        
        # 查看当前最大工号
        last_teacher = Teacher.query.filter(
            Teacher.id.like('T2025%')
        ).order_by(Teacher.id.desc()).first()
        
        if last_teacher:
            print(f"当前最大工号: {last_teacher.id}")
        
        # 生成新工号
        new_id = _generate_teacher_id()
        print(f"生成的新工号: {new_id}")
        
        return new_id

def test_teacher_approval():
    """测试教师申请审批"""
    import pymysql
    from datetime import datetime
    
    print("\n=== 模拟教师申请审批流程 ===")
    
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # 查找待审核的教师申请
        cursor.execute('''
            SELECT id, name FROM registration_applications 
            WHERE application_type = 'teacher' AND status = '待审核'
            ORDER BY id DESC LIMIT 1
        ''')
        
        app_record = cursor.fetchone()
        if app_record:
            app_id, teacher_name = app_record
            print(f"找到待审核申请: ID={app_id}, 姓名={teacher_name}")
            
            # 生成教师工号
            with app.app_context():
                new_teacher_id = test_teacher_id_generation()
            
            # 模拟审批通过
            cursor.execute('''
                UPDATE registration_applications 
                SET status = '已通过', 
                    assigned_id = %s, 
                    initial_password = '123456',
                    review_time = %s,
                    review_comments = '申请材料完整，符合录用条件，审批通过。'
                WHERE id = %s
            ''', (new_teacher_id, datetime.now(), app_id))
            
            print(f"申请审批完成: {teacher_name} -> {new_teacher_id}")
            
            conn.commit()
            
        else:
            print("没有找到待审核的教师申请")
        
        # 显示所有教师申请状态
        cursor.execute('''
            SELECT id, name, assigned_id, status, application_type 
            FROM registration_applications 
            WHERE application_type = 'teacher'
            ORDER BY id
        ''')
        
        print("\n=== 所有教师申请状态 ===")
        apps = cursor.fetchall()
        for app in apps:
            print(f"ID: {app[0]}, 姓名: {app[1]}, 工号: {app[2]}, 状态: {app[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == '__main__':
    test_teacher_approval()
    print("\n=== 测试完成 ===")
    print("现在可以访问 http://127.0.0.1:5000/register/status 查看申请状态")
