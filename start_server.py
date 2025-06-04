#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动Flask服务器脚本
"""
import os
import sys

def main():
    # 确保在正确的目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 添加当前目录到Python路径
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    print("学籍管理系统启动中...")
    print("=" * 50)
    
    try:
        print("正在检查数据库...")
        # 尝试初始化数据库（如果需要的话）
        from education_system.init_db import init_db
        # 只有在数据库为空时才初始化
        try:
            from education_system import get_db
            with get_db() as db:
                # 检查用户表是否存在
                result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchone()
                if not result:
                    print("数据库为空，正在初始化...")
                    init_db()
                    print("✅ 数据库初始化成功！")
                else:
                    print("✅ 数据库已存在，跳过初始化")
        except Exception as e:
            print(f"数据库检查时出错: {e}")
            print("尝试重新初始化数据库...")
            init_db()
            print("✅ 数据库重新初始化成功！")
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        print("系统将继续启动，但可能无法正常使用")
    
    print("\n🚀 启动Flask服务器...")
    print("📍 服务器地址: http://127.0.0.1:5000")
    print("\n🔑 测试账户信息:")
    print("=" * 50)
    print("👨‍💼 管理员账户:")
    print("   用户名: admin001")
    print("   密码: admin123")
    print("\n👨‍🏫 教师账户:")
    print("   用户名: T20250001")
    print("   密码: teacher123")
    print("   或者: T20250002 / teacher123")
    print("\n🧑‍🎓 学生账户:")
    print("   用户名: S20230001")
    print("   密码: student123")
    print("   或者: S20230002 / student123")
    print("=" * 50)
    print("\n✨ 新功能亮点:")
    print("   📊 教师成绩管理系统")
    print("   🎯 实时GPA计算")
    print("   💾 批量成绩保存")
    print("   📈 成绩统计分析")
    print("=" * 50)
    print("\n⚠️  按 Ctrl+C 停止服务器")
    print("🌐 请在浏览器中打开上述地址开始使用")
    print("-" * 50)
    
    try:
        # 启动Flask应用
        from education_system import app
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        print("请检查是否有其他程序占用5000端口")
        input("按回车键退出...")

if __name__ == '__main__':
    main()
