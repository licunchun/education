#!/usr/bin/env python3
# 最小化诊断脚本

print("开始诊断...")

try:
    print("1. 测试Flask导入...")
    from flask import Flask
    print("✅ Flask导入成功")
    
    print("2. 测试PyMySQL导入...")
    import pymysql
    print("✅ PyMySQL导入成功")
    
    print("3. 测试数据库连接...")
    import os
    DB_PASSWORD = '87893986lcc'
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password=DB_PASSWORD,
        database='education_system',
        charset='utf8mb4'
    )
    print("✅ 数据库连接成功")
    connection.close()
    
    print("4. 测试应用初始化...")
    import sys
    sys.path.insert(0, 'c:/Users/lcc/Desktop/education')
    
    # 逐步测试应用初始化
    from education_system import app
    print("✅ 应用导入成功")
    
    print("5. 测试数据库初始化...")
    from education_system import db
    print("✅ 数据库对象创建成功")
    
    print("6. 测试模型导入...")
    from education_system.models.database import User, Student
    print("✅ 模型导入成功")
    
    print("7. 测试路由文件...")
    from education_system import routes
    print("✅ 路由导入成功")
    
    print("8. 测试简单请求...")
    with app.test_client() as client:
        response = client.get('/')
        print(f"✅ 首页响应状态: {response.status_code}")
        print(f"响应长度: {len(response.data)} 字节")
        if response.status_code != 200:
            print(f"响应内容: {response.data.decode('utf-8')[:200]}")
    
    print("\n🎉 所有检查通过！")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    print(f"详细错误: {traceback.format_exc()}")
