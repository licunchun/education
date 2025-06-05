#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学籍管理系统功能测试脚本
测试所有核心功能是否正常工作
"""

import requests
import json
import time
from datetime import datetime

# 测试配置
BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

class SystemTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            'name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_homepage(self):
        """测试首页访问"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200 and "学籍管理系统" in response.text:
                self.log_test("首页访问", True, "页面正常加载")
                return True
            else:
                self.log_test("首页访问", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("首页访问", False, f"异常: {str(e)}")
            return False
    
    def test_student_login(self):
        """测试学生登录功能"""
        try:
            # 访问登录页面
            login_page = self.session.get(f"{self.base_url}/student/login")
            if login_page.status_code != 200:
                self.log_test("学生登录页面", False, f"页面加载失败: {login_page.status_code}")
                return False
            
            # 执行登录
            login_data = {
                'student_id': 'S20230001',
                'password': 'student123'
            }
            response = self.session.post(f"{self.base_url}/student/login", data=login_data)
            
            if response.status_code == 200 and "控制面板" in response.text:
                self.log_test("学生登录", True, "登录成功并跳转到仪表板")
                return True
            else:
                self.log_test("学生登录", False, f"登录失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("学生登录", False, f"异常: {str(e)}")
            return False
    
    def test_student_courses(self):
        """测试学生选课功能"""
        try:
            response = self.session.get(f"{self.base_url}/student/courses")
            if response.status_code == 200 and "选课系统" in response.text:
                self.log_test("学生选课页面", True, "选课页面正常访问")
                return True
            else:
                self.log_test("学生选课页面", False, f"页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("学生选课页面", False, f"异常: {str(e)}")
            return False
    
    def test_student_grades(self):
        """测试学生成绩查询功能"""
        try:
            response = self.session.get(f"{self.base_url}/student/grades")
            if response.status_code == 200 and "成绩查询" in response.text:
                self.log_test("学生成绩查询", True, "成绩查询页面正常访问")
                return True
            else:
                self.log_test("学生成绩查询", False, f"页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("学生成绩查询", False, f"异常: {str(e)}")
            return False
    
    def test_teacher_login(self):
        """测试教师登录功能"""
        try:
            # 先退出当前会话
            self.session.get(f"{self.base_url}/logout")
            
            # 教师登录
            login_data = {
                'teacher_id': 'T20250001',
                'password': 'teacher123'
            }
            response = self.session.post(f"{self.base_url}/teacher/login", data=login_data)
            
            if response.status_code == 200 and "控制面板" in response.text:
                self.log_test("教师登录", True, "教师登录成功")
                return True
            else:
                self.log_test("教师登录", False, f"登录失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("教师登录", False, f"异常: {str(e)}")
            return False
    
    def test_teacher_course_management(self):
        """测试教师课程管理"""
        try:
            response = self.session.get(f"{self.base_url}/teacher/course_management")
            if response.status_code == 200 and "课程管理" in response.text:
                self.log_test("教师课程管理", True, "课程管理页面正常访问")
                return True
            else:
                self.log_test("教师课程管理", False, f"页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("教师课程管理", False, f"异常: {str(e)}")
            return False
    
    def test_teacher_grade_management(self):
        """测试教师成绩管理"""
        try:
            response = self.session.get(f"{self.base_url}/teacher/grade_management")
            if response.status_code == 200 and "成绩管理" in response.text:
                self.log_test("教师成绩管理", True, "成绩管理页面正常访问")
                return True
            else:
                self.log_test("教师成绩管理", False, f"页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("教师成绩管理", False, f"异常: {str(e)}")
            return False
    
    def test_admin_login(self):
        """测试管理员登录功能"""
        try:
            # 先退出当前会话
            self.session.get(f"{self.base_url}/logout")
            
            # 管理员登录
            login_data = {
                'admin_id': 'admin001',
                'password': 'admin123'
            }
            response = self.session.post(f"{self.base_url}/admin/login", data=login_data)
            
            if response.status_code == 200 and "控制面板" in response.text:
                self.log_test("管理员登录", True, "管理员登录成功")
                return True
            else:
                self.log_test("管理员登录", False, f"登录失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("管理员登录", False, f"异常: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始系统功能测试")
        print("=" * 50)
        
        # 基础功能测试
        print("\n📋 基础功能测试:")
        self.test_homepage()
        
        # 学生功能测试
        print("\n🧑‍🎓 学生功能测试:")
        if self.test_student_login():
            self.test_student_courses()
            self.test_student_grades()
        
        # 教师功能测试
        print("\n👨‍🏫 教师功能测试:")
        if self.test_teacher_login():
            self.test_teacher_course_management()
            self.test_teacher_grade_management()
        
        # 管理员功能测试
        print("\n👨‍💼 管理员功能测试:")
        self.test_admin_login()
        
        # 输出测试总结
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "=" * 50)
        print("📊 测试总结")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['success']])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for test in self.test_results:
                if not test['success']:
                    print(f"  - {test['name']}: {test['message']}")
        
        print("\n" + "=" * 50)
        print("测试完成！")

def main():
    """主函数"""
    print("🎓 学籍管理系统功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试目标: {BASE_URL}")
    
    # 等待服务器启动
    print("\n⏳ 等待服务器启动...")
    time.sleep(2)
    
    # 运行测试
    tester = SystemTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
