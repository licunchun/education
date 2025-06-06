#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime, date

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from education_system import create_app, db
from education_system.models.database import Tuition

def add_deadlines():
    """为学费记录添加截止日期"""
    app = create_app()
    
    with app.app_context():
        print("开始为学费记录添加截止日期...")
        
        # 获取所有没有截止日期的学费记录
        tuitions = Tuition.query.filter(Tuition.deadline.is_(None)).all()
        
        print(f"找到 {len(tuitions)} 条需要添加截止日期的学费记录")
        
        for tuition in tuitions:
            # 根据学年设置截止日期
            # 假设学年格式为 "2024-2025"
            year_parts = tuition.academic_year.split('-')
            if len(year_parts) == 2:
                start_year = int(year_parts[0])
                
                if tuition.semester == '第一学期':
                    # 第一学期截止日期：开学年份的12月31日
                    deadline = date(start_year, 12, 31)
                elif tuition.semester == '第二学期':
                    # 第二学期截止日期：结束年份的6月30日
                    end_year = int(year_parts[1])
                    deadline = date(end_year, 6, 30)
                else:
                    # 全年缴费截止日期：结束年份的6月30日
                    end_year = int(year_parts[1])
                    deadline = date(end_year, 6, 30)
                
                tuition.deadline = deadline
                print(f"  学生 {tuition.student_id} {tuition.academic_year} {tuition.semester} 截止日期设为: {deadline}")
        
        # 提交更改
        try:
            db.session.commit()
            print(f"成功为 {len(tuitions)} 条学费记录添加截止日期!")
        except Exception as e:
            db.session.rollback()
            print(f"添加截止日期时出错: {e}")

if __name__ == '__main__':
    add_deadlines()
