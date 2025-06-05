#!/usr/bin/env python3
# 测试白屏问题的脚本

import requests
import sys

def test_page(url, description):
    """测试页面是否正常响应"""
    try:
        print(f"🔍 测试 {description}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            if len(content) > 100 and '<html' in content and '</html>' in content:
                print(f"✅ {description} - 正常 (长度: {len(content)} 字符)")
                return True
            else:
                print(f"❌ {description} - 内容异常 (长度: {len(content)} 字符)")
                print(f"   前100字符: {content[:100]}")
                return False
        else:
            print(f"❌ {description} - HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description} - 错误: {e}")
        return False

def main():
    print("🎓 学籍管理系统 - 白屏问题检测")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # 测试页面列表
    test_pages = [
        (f"{base_url}/", "首页"),
        (f"{base_url}/student/login", "学生登录页"),
        (f"{base_url}/teacher/login", "教师登录页"),
        (f"{base_url}/admin/login", "管理员登录页"),
    ]
    
    print("📋 测试页面访问...")
    all_passed = True
    
    for url, desc in test_pages:
        if not test_page(url, desc):
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ 所有页面测试通过！")
        print("\n🌐 现在测试登录后的页面...")
        
        # 测试登录功能
        test_login()
    else:
        print("❌ 部分页面存在问题，请检查Flask服务器日志")

def test_login():
    """测试登录功能"""
    session = requests.Session()
    
    # 测试学生登录
    print("\n🧑‍🎓 测试学生登录...")
    login_data = {
        'student_id': 'S20230001',
        'password': 'student123'
    }
    
    try:
        response = session.post('http://127.0.0.1:5000/student/login', data=login_data)
        if response.status_code == 200 and 'dashboard' in response.url:
            print("✅ 学生登录成功")
            
            # 测试学生dashboard
            dashboard_response = session.get('http://127.0.0.1:5000/student/dashboard')
            if dashboard_response.status_code == 200:
                print("✅ 学生控制面板正常")
            else:
                print(f"❌ 学生控制面板错误: {dashboard_response.status_code}")
        else:
            print(f"❌ 学生登录失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 学生登录测试错误: {e}")

if __name__ == "__main__":
    main()
