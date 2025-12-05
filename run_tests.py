# -*- coding: utf-8 -*-
"""
测试执行脚本
提供便捷的测试执行方式
"""
import os
import sys
import subprocess
from config.config import ALLURE_REPORT_DIR, REPORT_DIR


def run_tests(args=''):
    """
    运行测试
    :param args: 额外的pytest参数
    """
    print("=" * 80)
    print("开始执行测试...")
    print("=" * 80)
    
    # 构建pytest命令
    cmd = f'pytest {args}'
    
    # 执行测试
    result = subprocess.run(cmd, shell=True)
    
    return result.returncode


def generate_allure_report():
    """生成并打开Allure报告"""
    print("\n" + "=" * 80)
    print("生成Allure报告...")
    print("=" * 80)
    
    allure_results = os.path.join(REPORT_DIR, 'allure')
    allure_report = os.path.join(REPORT_DIR, 'allure-report')
    
    # 生成报告
    cmd = f'allure generate {allure_results} -o {allure_report} --clean'
    subprocess.run(cmd, shell=True)
    
    print("\n正在打开Allure报告...")
    # 打开报告
    cmd = f'allure open {allure_report}'
    subprocess.run(cmd, shell=True)

def main():
    """主函数"""
    print("""
    ╔════════════════════════════════════════════════╗
    ║     登录功能自动化测试执行脚本                  ║
    ╚════════════════════════════════════════════════╝
    
    请选择执行方式:
    1. 运行所有测试
    2. 运行数据驱动测试（Excel）
    3. 运行正向测试
    4. 运行异常测试
    5. 运行指定用例（输入用例ID）
    6. 仅生成Allure报告
    0. 退出
    """)
    
    choice = input("请输入选项 (0-6): ").strip()
    
    if choice == '1':
        run_tests()
        generate_allure_report()
        
    elif choice == '2':
        run_tests('tests/test_login.py::TestLogin')
        generate_allure_report()
        
    elif choice == '3':
        run_tests('tests/test_login.py::TestLoginPositive')
        generate_allure_report()
        
    elif choice == '4':
        run_tests('tests/test_login.py::TestLoginNegative')
        generate_allure_report()
        
    elif choice == '5':
        case_id = input("请输入用例ID (例如: TC001): ").strip()
        run_tests(f'tests/test_login.py -k {case_id}')
        generate_allure_report()
        
    elif choice == '6':
        generate_allure_report()
        
    elif choice == '0':
        print("退出程序")
        sys.exit(0)
        
    else:
        print("无效的选项!")
        sys.exit(1)


if __name__ == '__main__':
    main()
