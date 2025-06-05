#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录功能
"""
import requests
import sys

def test_login(login_type, username, password):
    """测试登录功能"""
    base_url = "http://127.0.0.1:5000"
    
    # 创建会话
    session = requests.Session()
    
    # 获取登录页面
    login_url = f"{base_url}/{login_type}/login"
    response = session.get(login_url)
    
    if response.status_code != 200:
        print(f"❌ 无法访问登录页面: {login_url}")
        return False
    
    print(f"✅ 登录页面访问正常: {login_url}")
    
    # 准备登录数据
    if login_type == "student":
        login_data = {
            'student_id': username,
            'password': password
        }
    elif login_type == "teacher":
        login_data = {
            'teacher_id': username,
            'password': password
        }
    else:  # admin
        login_data = {
            'admin_id': username,
            'password': password
        }
    
    # 提交登录
    response = session.post(login_url, data=login_data, allow_redirects=False)
    
    if response.status_code == 302:  # 重定向表示登录成功
        print(f"✅ 登录成功，重定向到: {response.headers.get('Location', 'unknown')}")
        
        # 访问dashboard
        dashboard_url = f"{base_url}/{login_type}/dashboard"
        dashboard_response = session.get(dashboard_url)
        
        if dashboard_response.status_code == 200:
            print(f"✅ Dashboard访问成功")
            if "UndefinedError" in dashboard_response.text:
                print(f"❌ Dashboard有模板错误")
                return False
            else:
                print(f"✅ Dashboard模板正常")
                return True
        else:
            print(f"❌ Dashboard访问失败: {dashboard_response.status_code}")
            return False
    else:
        print(f"❌ 登录失败: {response.status_code}")
        print(f"响应内容: {response.text[:200]}...")
        return False

def main():
    print("🚀 开始测试登录功能...")
    
    # 测试用例
    test_cases = [
        ("student", "S20230001", "student123"),
        ("teacher", "T20250001", "teacher123"),
        ("admin", "admin001", "admin123")
    ]
    
    all_passed = True
    
    for login_type, username, password in test_cases:
        print(f"\n📝 测试 {login_type} 登录...")
        result = test_login(login_type, username, password)
        if not result:
            all_passed = False
    
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 所有登录测试通过！")
    else:
        print("❌ 部分登录测试失败！")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
