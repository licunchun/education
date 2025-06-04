from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Flask测试成功！</h1><p>服务器正在正常运行</p>'

if __name__ == '__main__':
    print("正在启动测试服务器...")
    print("访问 http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
