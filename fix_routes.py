# 修复routes.py中的主要问题
import re

def fix_routes_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修复缩进问题（注释前的额外空格）
    content = re.sub(r'(\s+)#(\s+)', r'        # ', content)
    
    # 2. 修复数据库查询结果的访问方式（统一使用索引访问）
    # 将.password改为['password']等
    content = re.sub(r'(\w+)\.(\w+)', r'\1["\2"]', content)

    # 保存修复后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复 {file_path}")

if __name__ == "__main__":
    fix_routes_file("c:/Users/lcc/Desktop/education/education_system/routes.py")
