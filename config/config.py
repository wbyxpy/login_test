# -*- coding: utf-8 -*-
"""
配置文件
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试数据配置
TEST_DATA_DIR = os.path.join(BASE_DIR, 'test_data')
TEST_DATA_FILE = os.path.join(TEST_DATA_DIR, 'login_test_cases.xlsx')

# 测试报告配置
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
ALLURE_REPORT_DIR = os.path.join(REPORT_DIR, 'allure')
HTML_REPORT_DIR = os.path.join(REPORT_DIR, 'html')

# 截图配置
SCREENSHOT_DIR = os.path.join(REPORT_DIR, 'screenshots')

# 浏览器配置
BROWSER = 'chrome'  # 支持: chrome, firefox, edge
HEADLESS = False  # 是否无头模式
IMPLICIT_WAIT = 10  # 隐式等待时间(秒)
PAGE_LOAD_TIMEOUT = 30  # 页面加载超时时间(秒)

# 登录页面URL
LOGIN_URL = 'http://192.168.5.113:3000/login'

# 超级管理员账号信息（用于验证）
SUPER_ADMIN = {
    'username': 'admin',
    'password': 'user123456'
}

# 错误提示信息
ERROR_MESSAGE = '请检查输入的账号或密码是否正确'
ERROR_MESSAGE_DISPLAY_TIME = 1  # 错误提示展示时间(秒)
