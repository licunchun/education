#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL数据库设置助手
用于帮助配置和测试MySQL数据库连接
"""
import pymysql
import sys
import os

def test_mysql_connection():
    """测试MySQL连接"""
    print("🔍 测试MySQL数据库连接...")
    
    # 从环境变量或默认值获取连接信息
    host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', '3306'))
    user = os.environ.get('DB_USER', 'root')
    password = os.environ.get('DB_PASSWORD', 'your_password_here')
    database = os.environ.get('DB_NAME', 'education_system')
    
    try:
        # 先连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        print(f"✅ 成功连接到MySQL服务器 {host}:{port}")
        
        # 检查数据库是否存在
        cursor.execute(f"SHOW DATABASES LIKE '{database}'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print(f"⚠️  数据库 '{database}' 不存在，正在创建...")
            cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ 数据库 '{database}' 创建成功")
        else:
            print(f"✅ 数据库 '{database}' 已存在")
        
        # 测试连接到指定数据库
        connection.select_db(database)
        print(f"✅ 成功连接到数据库 '{database}'")
        
        # 显示数据库版本
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"📊 MySQL版本: {version}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        print("\n💡 请检查以下配置:")
        print(f"   主机: {host}")
        print(f"   端口: {port}")
        print(f"   用户: {user}")
        print(f"   密码: {'*' * len(password) if password else '(未设置)'}")
        print(f"   数据库: {database}")
        print("\n🔧 解决方案:")
        print("1. 确保MySQL服务已启动")
        print("2. 检查用户名和密码是否正确")
        print("3. 确保用户有创建数据库的权限")
        print("4. 检查防火墙设置")
        return False

def setup_environment():
    """设置环境变量"""
    print("\n🔧 MySQL数据库配置")
    print("=" * 50)
    
    host = input("MySQL主机地址 [localhost]: ").strip() or 'localhost'
    port = input("MySQL端口 [3306]: ").strip() or '3306'
    user = input("MySQL用户名 [root]: ").strip() or 'root'
    password = input("MySQL密码: ").strip()
    database = input("数据库名 [education_system]: ").strip() or 'education_system'
    
    print(f"\n📝 配置信息:")
    print(f"   主机: {host}")
    print(f"   端口: {port}")
    print(f"   用户: {user}")
    print(f"   密码: {'*' * len(password) if password else '(未设置)'}")
    print(f"   数据库: {database}")
    
    # 设置环境变量
    os.environ['DB_HOST'] = host
    os.environ['DB_PORT'] = port
    os.environ['DB_USER'] = user
    os.environ['DB_PASSWORD'] = password
    os.environ['DB_NAME'] = database
    
    return test_mysql_connection()

def main():
    """主函数"""
    print("🎓 学生管理系统 - MySQL数据库设置")
    print("=" * 50)
    
    # 检查PyMySQL是否已安装
    try:
        import pymysql
        print("✅ PyMySQL已安装")
    except ImportError:
        print("❌ PyMySQL未安装")
        print("📦 请先安装PyMySQL: pip install PyMySQL")
        return
    
    # 选择配置方式
    print("\n选择配置方式:")
    print("1. 使用默认配置测试连接")
    print("2. 手动配置数据库连接")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == '1':
        if test_mysql_connection():
            print("\n🎉 数据库连接测试成功！")
            print("💡 您现在可以运行 python app.py 启动应用")
        else:
            print("\n❌ 连接测试失败，请检查配置")
    elif choice == '2':
        if setup_environment():
            print("\n🎉 数据库配置和连接测试成功！")
            print("💡 您现在可以运行 python app.py 启动应用")
        else:
            print("\n❌ 配置失败，请重新检查")
    elif choice == '3':
        print("👋 再见！")
    else:
        print("❌ 无效选择")

if __name__ == '__main__':
    main()
