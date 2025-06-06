#!/usr/bin/env python3
# 超简单Flask测试

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hello World!</h1><p>这是一个简单的测试页面</p>"

@app.route('/test')
def test():
    return jsonify({"status": "ok", "message": "测试成功"})

if __name__ == '__main__':
    print("启动简单Flask应用...")
    app.run(debug=True, host='127.0.0.1', port=5001)
