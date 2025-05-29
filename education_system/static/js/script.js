// 主脚本文件
document.addEventListener('DOMContentLoaded', function() {
    console.log('学籍管理系统已加载');
    
    // 表单验证
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let valid = true;
            const inputs = form.querySelectorAll('input[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('请填写所有必填字段');
            }
        });
    });
});
