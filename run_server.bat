@echo off
echo 正在启动学生管理系统...
cd /d "%~dp0"
python -c "from education_system import app; app.run(host='127.0.0.1', port=5000, debug=True)"
pause
