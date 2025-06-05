#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查MySQL数据库数据
"""
import pymysql

def check_db_data():
    """检查数据库中的数据"""
    try:
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='87893986lcc',
            database='education_system',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 检查各表的数据量
        tables = ['users', 'roles', 'students', 'teachers', 'majors', 'classes', 'courses']
        
        print("📊 数据库表数据统计:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} 条记录")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                rows = cursor.fetchall()
                print(f"     示例数据: {rows[0] if rows else '无'}")
        
        cursor.close()
        connection.close()
        print("✅ 数据检查完成")
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")

if __name__ == '__main__':
    check_db_data()
