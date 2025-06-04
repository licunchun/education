#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Flask应用启动
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("正在导入Flask...")
    from flask import Flask
    print("✅ Flask导入成功")
    
    print("正在导入应用模块...")
    from education_system import app
    print("✅ 应用模块导入成功")
    
    print("正在测试数据库连接...")
    from education_system import get_db
    with get_db() as db:
        result = db.execute("SELECT COUNT(*) FROM students").fetchone()
        print(f"✅ 数据库连接成功，学生数量: {result[0]}")
        
        result = db.execute("SELECT COUNT(*) FROM offered_courses").fetchone()
        print(f"✅ 开课数量: {result[0]}")
        
        result = db.execute("SELECT COUNT(*) FROM course_selections").fetchone()
        print(f"✅ 选课记录数量: {result[0]}")
    
    print("正在启动服务器...")
    print("🌐 服务器将在 http://127.0.0.1:5000 启动")
    print("⚠️  按 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
    
except Exception as e:
    print(f"❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
    input("按回车键退出...")
