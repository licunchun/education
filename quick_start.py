#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动和测试脚本
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 启动学生管理系统...")
    print("=" * 50)
    
    try:
        # 导入应用
        from education_system import app
        
        print("✅ 应用导入成功")
        print("🌐 服务器将在 http://127.0.0.1:5000 启动")
        print("\n🔑 测试账户:")
        print("学生账户: S20230001 / student123")
        print("教师账户: T20250001 / teacher123") 
        print("管理员账户: admin001 / admin123")
        print("=" * 50)
        print("⚠️  按 Ctrl+C 停止服务器")
        print("🔧 已修复学生选课和成绩查询的问题")
        
        # 启动服务器
        app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
        
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
