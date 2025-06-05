#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hello World!</h1><p>Flask is working correctly.</p>"

@app.route('/test')
def test():
    return "<h1>Test Page</h1><p>This is a test page.</p>"

if __name__ == '__main__':
    print("🚀 启动超简单Flask服务器...")
    print("📍 访问地址: http://127.0.0.1:5002")
    app.run(host='127.0.0.1', port=5002, debug=True)
