#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学籍管理系统 - 主启动文件
启动Flask应用，自动检查MySQL数据库
"""
import os
import sys

def main():
    """主启动函数"""
    # 确保在正确的目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 添加当前目录到Python路径
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    print("🎓 学生管理系统 - MySQL版本")
    print("=" * 50)
    
    try:
        # 检查依赖包
        print("📋 检查依赖包...")
        try:
            import pymysql
            from sqlalchemy import text
            from flask import Flask
            from flask_sqlalchemy import SQLAlchemy
            print("✅ 所有依赖包已安装")
        except ImportError as e:
            print(f"❌ 依赖包未安装: {e}")
            print("📦 请运行: pip install -r requirements.txt")
            input("按回车键退出...")
            return
        
        # 检查并初始化数据库
        print("📋 正在检查MySQL数据库...")
        from education_system import app, db
        
        # 检查数据库连接和表是否存在
        try:
            with app.app_context():
                with db.engine.connect() as connection:
                    result = connection.execute(text("SHOW TABLES LIKE 'users'"))
                    if not result.fetchone():
                        print("🔧 数据库表不存在，正在初始化...")
                        # 运行数据插入脚本
                        exec(open('insert_data.py').read())
                        print("✅ MySQL数据库初始化成功！")
                    else:
                        print("✅ MySQL数据库表已存在")
        except Exception as e:
            print(f"⚠️  数据库连接失败: {e}")
            print("🔧 请检查MySQL配置和连接")
            print("📦 或检查MySQL服务是否启动")
            print("💡 您可以运行 python setup_mysql.py 重新配置")
            input("按回车键退出...")
            return
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        print("系统将尝试继续启动...")
    
    # 显示登录信息
    print("\n🔑 系统账户信息:")
    print("=" * 50)
    print("👨‍💼 管理员账户:")
    print("   用户名: admin001")
    print("   密码: admin123")
    print("\n👨‍🏫 教师账户:")
    print("   用户名: T20250001")
    print("   密码: teacher123")
    print("\n🧑‍🎓 学生账户:")
    print("   用户名: S20230001")
    print("   密码: student123")
    print("=" * 50)
    
    print("\n🚀 启动Flask服务器...")
    print("📍 服务器地址: http://127.0.0.1:5000")
    print("\n✨ 系统功能:")
    print("   📊 学生/教师管理")
    print("   🎯 成绩管理系统") 
    print("   📝 注册审批流程")
    print("   📈 数据统计分析")
    print("   🗄️  MySQL数据库支持")
    print("=" * 50)
    print("\n⚠️  按 Ctrl+C 停止服务器")
    print("🌐 请在浏览器中打开上述地址开始使用")
    print("-" * 50)
    
    try:
        # 启动Flask应用
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        print("请检查是否有其他程序占用5000端口")
        input("按回车键退出...")

if __name__ == '__main__':
    main()