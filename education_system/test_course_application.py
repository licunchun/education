#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课程申请功能测试
"""
import pymysql
from datetime import datetime
import sys
import os

# 添加项目根目录到路径，确保可以导入education_system模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_course_application_feature():
    """测试课程申请功能"""
    try:
        print("正在连接MySQL数据库...")
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='87893986lcc',
            database='education_system'
        )
        cursor = conn.cursor()
        print("✅ 数据库连接成功")
        
        # 1. 验证课程申请表是否存在
        cursor.execute("SHOW TABLES LIKE 'course_applications'")
        if not cursor.fetchone():
            print("❌ 测试失败：课程申请表不存在")
            return False
        
        print("✅ 课程申请表存在")
        
        # 2. 验证相关路由是否存在
        from education_system import app
        routes = [rule.endpoint for rule in app.url_map.iter_rules()]
        
        required_routes = [
            'teacher_course_application',
            'admin_course_applications',
            'admin_course_application_approve',
            'admin_course_application_reject'
        ]
        
        missing_routes = [route for route in required_routes if route not in routes]
        if missing_routes:
            print(f"❌ 测试失败：缺少以下路由：{missing_routes}")
            return False
        
        print("✅ 所有必要的路由都存在")
        
        # 3. 测试数据插入 - 创建一个测试申请
        test_teacher_id = None
        cursor.execute("SELECT id FROM teachers LIMIT 1")
        result = cursor.fetchone()
        if result:
            test_teacher_id = result[0]
        else:
            print("❌ 测试失败：找不到教师数据")
            return False
        
        test_course_id = None
        cursor.execute("SELECT id FROM courses LIMIT 1")
        result = cursor.fetchone()
        if result:
            test_course_id = result[0]
        else:
            print("❌ 测试失败：找不到课程数据")
            return False
        
        # 先清理可能存在的测试数据
        cursor.execute("DELETE FROM course_applications WHERE application_note = '测试申请，请忽略'")
        conn.commit()
        
        # 插入测试申请
        insert_sql = """
        INSERT INTO course_applications 
        (teacher_id, course_id, academic_year, semester, schedule, location, capacity, 
         application_note, application_time, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_sql, (
            test_teacher_id,
            test_course_id,
            '2025-2026',
            '第一学期',
            '周一1-2节',
            '教学楼A-101',
            60,
            '测试申请，请忽略',
            datetime.now(),
            '待审核'
        ))
        conn.commit()
        
        # 验证插入是否成功
        cursor.execute("SELECT id FROM course_applications WHERE application_note = '测试申请，请忽略'")
        if not cursor.fetchone():
            print("❌ 测试失败：无法插入课程申请数据")
            return False
        
        print("✅ 课程申请数据插入成功")
        
        # 清理测试数据
        cursor.execute("DELETE FROM course_applications WHERE application_note = '测试申请，请忽略'")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("✅ 所有测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == '__main__':
    print("=== 课程申请功能测试 ===\n")
    success = test_course_application_feature()
    if success:
        print("\n🎉 功能测试通过！课程申请功能可以正常使用。")
    else:
        print("\n❌ 功能测试失败，请检查错误信息。")
