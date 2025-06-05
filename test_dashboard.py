#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试dashboard路由
"""
from education_system import app, db
from education_system.models.database import Student, Teacher
from flask import session

def test_student_dashboard():
    """测试学生dashboard"""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['student_id'] = 'S20230001'
            sess['user_type'] = 'student'
            sess['user_id'] = 4
            sess['real_name'] = '张三'
        
        try:
            response = client.get('/student/dashboard')
            print(f"学生Dashboard状态码: {response.status_code}")
            if response.status_code == 200:
                print("✅ 学生Dashboard正常")
                return True
            else:
                print(f"❌ 学生Dashboard错误: {response.data.decode('utf-8')[:500]}")
                return False
        except Exception as e:
            print(f"❌ 学生Dashboard异常: {str(e)}")
            return False

def test_teacher_dashboard():
    """测试教师dashboard"""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['teacher_id'] = 'T20250001'
            sess['user_type'] = 'teacher'
            sess['user_id'] = 2
            sess['real_name'] = '李教授'
        
        try:
            response = client.get('/teacher/dashboard')
            print(f"教师Dashboard状态码: {response.status_code}")
            if response.status_code == 200:
                print("✅ 教师Dashboard正常")
                return True
            else:
                print(f"❌ 教师Dashboard错误: {response.data.decode('utf-8')[:500]}")
                return False
        except Exception as e:
            print(f"❌ 教师Dashboard异常: {str(e)}")
            return False

def test_admin_dashboard():
    """测试管理员dashboard"""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['admin_id'] = 'admin001'
            sess['user_type'] = 'admin'
            sess['user_id'] = 1
            sess['real_name'] = '张管理'
        
        try:
            response = client.get('/admin/dashboard')
            print(f"管理员Dashboard状态码: {response.status_code}")
            if response.status_code == 200:
                print("✅ 管理员Dashboard正常")
                return True
            else:
                print(f"❌ 管理员Dashboard错误: {response.data.decode('utf-8')[:500]}")
                return False
        except Exception as e:
            print(f"❌ 管理员Dashboard异常: {str(e)}")
            return False

if __name__ == "__main__":
    with app.app_context():
        print("🚀 开始测试Dashboard路由...")
        
        print("\n📝 测试学生Dashboard...")
        test_student_dashboard()
        
        print("\n📝 测试教师Dashboard...")
        test_teacher_dashboard()
        
        print("\n📝 测试管理员Dashboard...")
        test_admin_dashboard()
