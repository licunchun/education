from education_system import app, db
from education_system.models.database import RegistrationApplication

def check_applications():
    with app.app_context():
        try:
            # 查询所有申请
            applications = RegistrationApplication.query.all()
            print(f"总共找到 {len(applications)} 条申请记录")
            
            # 检查已通过的申请是否有账号信息
            approved_apps = [app for app in applications if app.status == '已通过']
            print(f"其中 {len(approved_apps)} 条已通过审核")
            
            for app in approved_apps:
                print(f"ID: {app.id}, 姓名: {app.name}, 类型: {app.application_type}, 状态: {app.status}")
                
                # 检查是否有账号信息
                if hasattr(app, 'assigned_id') and app.assigned_id:
                    print(f"  分配的ID: {app.assigned_id}")
                else:
                    print("  缺少分配的ID")
                
                if hasattr(app, 'initial_password') and app.initial_password:
                    print(f"  初始密码: {app.initial_password}")
                else:
                    print("  缺少初始密码")
                
                # 打印所有属性，用于调试
                print("  所有属性:")
                for attr_name in dir(app):
                    if not attr_name.startswith('_') and attr_name not in ['metadata', 'query', 'registry']:
                        try:
                            attr_value = getattr(app, attr_name)
                            if not callable(attr_value):
                                print(f"    {attr_name}: {attr_value}")
                        except Exception as e:
                            print(f"    {attr_name}: 无法获取值 ({str(e)})")
                
                print("\n")
                
        except Exception as e:
            print(f"检查申请记录时出错: {str(e)}")

if __name__ == "__main__":
    check_applications()
