# MySQL数据库迁移指南

## 从SQLite迁移到MySQL

### 1. 安装MySQL

#### Windows:
1. 下载MySQL Community Server: https://dev.mysql.com/downloads/mysql/
2. 安装并启动MySQL服务
3. 记住root用户的密码

#### macOS (使用Homebrew):
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库连接

有两种方式配置数据库连接：

#### 方式1: 使用环境变量
```bash
# Windows PowerShell
$env:DB_HOST="localhost"
$env:DB_PORT="3306" 
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="education_system"

# Windows CMD
set DB_HOST=localhost
set DB_PORT=3306
set DB_USER=root
set DB_PASSWORD=your_password
set DB_NAME=education_system

# Linux/macOS
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=education_system
```

#### 方式2: 运行配置脚本
```bash
python setup_mysql.py
```

### 4. 创建数据库

登录MySQL创建数据库：
```sql
mysql -u root -p
CREATE DATABASE education_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON education_system.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. 启动应用

```bash
python app.py
```

## 主要变化

### 1. 数据库驱动
- 从 `sqlite3` 改为 `PyMySQL`
- 支持SQLAlchemy ORM

### 2. 连接配置
- SQLite: 文件数据库
- MySQL: 网络数据库，需要连接字符串

### 3. 数据类型映射
- `INTEGER PRIMARY KEY AUTOINCREMENT` → `db.Integer, primary_key=True`
- `TEXT` → `db.String()` 或 `db.Text`
- `REAL` → `db.Float`
- `BOOLEAN` → `db.Boolean`

### 4. 字符集支持
- MySQL使用utf8mb4字符集，完整支持emoji和特殊字符
- 自动处理中文字符编码

## 性能优势

1. **并发性能**: MySQL支持更好的并发访问
2. **数据完整性**: 更强的事务支持和外键约束
3. **扩展性**: 支持集群和读写分离
4. **备份恢复**: 完善的备份和恢复机制

## 故障排除

### 连接失败
1. 检查MySQL服务是否启动
2. 确认用户名密码正确
3. 检查防火墙设置
4. 验证数据库是否存在

### 权限问题
```sql
GRANT ALL PRIVILEGES ON education_system.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### 字符编码问题
确保MySQL配置使用utf8mb4:
```ini
[mysqld]
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
```

## 数据备份

### 备份数据
```bash
mysqldump -u root -p education_system > backup.sql
```

### 恢复数据
```bash
mysql -u root -p education_system < backup.sql
```
