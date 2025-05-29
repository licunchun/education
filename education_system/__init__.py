# 初始化Flask应用
from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置密钥，用于会话

# 导入视图模块（放在这里是为了避免循环导入）
from education_system import routes
