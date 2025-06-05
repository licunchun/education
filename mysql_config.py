# MySQL数据库配置示例
# 请根据您的实际环境修改这些配置

# 数据库连接信息
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'education_system'
DB_USER = 'root'
DB_PASSWORD = 'your_password_here'

# 完整的数据库连接URL
DATABASE_URL = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# 创建数据库的SQL命令（需要先手动创建数据库）
# CREATE DATABASE education_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
