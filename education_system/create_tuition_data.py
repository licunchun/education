#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建示例学费数据脚本
为现有学生创建学费记录进行功能测试
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from education_system import app, db
from education_system.models.database import Student, Tuition
from datetime import datetime, date

def create_tuition_data():
    """为学生创建示例学费数据"""
    with app.app_context():
        try:
            # 获取所有学生
            students = Student.query.all()
            print(f"为 {len(students)} 个学生创建学费数据...")
            
            # 为每个学生创建学费记录
            for student in students:
                # 检查是否已经有学费记录
                existing = Tuition.query.filter_by(
                    student_id=student.id,
                    academic_year='2024-2025'
                ).first()
                
                if not existing:
                    # 创建2024-2025学年学费记录
                    tuition = Tuition(
                        student_id=student.id,
                        academic_year='2024-2025',
                        amount=8000.0,  # 学费8000元
                        paid_amount=0.0,
                        status='未缴费',
                        deadline=date(2025, 8, 31)  # 截止日期2025年8月31日
                    )
                    db.session.add(tuition)
                    print(f"✓ 为学生 {student.id}({student.name}) 创建学费记录")
                else:
                    print(f"○ 学生 {student.id}({student.name}) 已有学费记录")
            
            # 提交更改
            db.session.commit()
            print("\n✅ 学费数据创建完成！")
            
            # 统计信息
            total_tuitions = Tuition.query.count()
            unpaid_tuitions = Tuition.query.filter_by(status='未缴费').count()
            print(f"\n数据统计:")
            print(f"总学费记录数: {total_tuitions}")
            print(f"未缴费记录数: {unpaid_tuitions}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ 创建失败: {str(e)}")

if __name__ == '__main__':
    print("开始创建示例学费数据")
    print("=" * 50)
    create_tuition_data()
