#!/usr/bin/env python3
# 测试应用响应

import requests
import time

print("测试应用连接...")

try:
    # 测试基本连接
    print("1. 测试根路径...")
    response = requests.get('http://127.0.0.1:5000', timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    if response.status_code == 200:
        print(f"响应长度: {len(response.text)} 字符")
        print(f"响应前100字符: {response.text[:100]}")
    else:
        print(f"错误响应: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ 连接超时")
except requests.exceptions.ConnectionError as e:
    print(f"❌ 连接错误: {e}")
except Exception as e:
    print(f"❌ 其他错误: {e}")

print("\n2. 测试静态文件...")
try:
    response = requests.get('http://127.0.0.1:5000/static/css/style.css', timeout=5)
    print(f"CSS文件状态: {response.status_code}")
except Exception as e:
    print(f"CSS文件错误: {e}")
