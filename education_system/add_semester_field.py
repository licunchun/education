#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为学费表添加semester字段的数据库迁移脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from education_system import db, app
from education_system.models.database import Tuition

def add_semester_field():
    """为学费表添加semester字段并初始化"""
    with app.app_context():
        try:
            from sqlalchemy import text
            
            # 检查是否已经有semester字段
            with db.engine.connect() as connection:
                result = connection.execute(text("SHOW COLUMNS FROM tuitions LIKE 'semester'"))
                columns = list(result)
                
                if not columns:
                    print("添加semester字段...")
                    # 添加字段（MySQL语法）
                    connection.execute(text("ALTER TABLE tuitions ADD COLUMN semester VARCHAR(20) DEFAULT '全年'"))
                    connection.commit()
                    print("✓ semester字段添加成功")
                else:
                    print("semester字段已存在")
            
            # 更新所有现有学费记录的semester字段
            tuitions = Tuition.query.filter(Tuition.semester.is_(None)).all()
            if tuitions:
                print(f"初始化 {len(tuitions)} 条学费记录的学期信息...")
                for tuition in tuitions:
                    tuition.semester = '全年'
                db.session.commit()
                print("✓ 学费记录学期信息初始化完成")
            else:
                print("所有学费记录学期信息已初始化")
            
            # 验证结果
            total_tuitions = Tuition.query.count()
            print(f"\n数据统计:")
            print(f"总学费记录数: {total_tuitions}")
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("开始数据库迁移：为学费表添加semester字段")
    print("=" * 50)
    add_semester_field()
    print("✅ 数据库迁移完成！")
