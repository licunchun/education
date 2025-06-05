#!/usr/bin/env python3
# 最小化Flask测试 - 用于调试白屏问题

from flask import Flask
import sys
import os

# 添加项目目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 开始最小化调试...")

try:
    print("1. 测试Flask导入...")
    from flask import Flask
    print("✅ Flask导入成功")
    
    print("2. 测试education_system导入...")
    from education_system import app, db
    print("✅ education_system导入成功")
    
    print("3. 测试数据库模型导入...")
    from education_system.models.database import User, Student, Teacher
    print("✅ 数据库模型导入成功")
    
    print("4. 测试routes导入...")
    from education_system import routes
    print("✅ routes导入成功")
    
    print("5. 测试数据库连接...")
    with app.app_context():
        try:
            users_count = User.query.count()
            print(f"✅ 数据库连接成功，用户数量: {users_count}")
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
    
    print("6. 测试Flask应用...")
    
    @app.route('/test')
    def test_route():
        return "Test OK"
    
    print("✅ 所有组件加载成功")
    print("🚀 启动测试服务器...")
    
    if __name__ == '__main__':
        app.run(host='127.0.0.1', port=5001, debug=True)
        
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ 其他错误: {e}")
    sys.exit(1)
