# # -*- coding: utf-8 -*-
"""
pytest配置文件
定义fixtures和钩子函数
"""
import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime

from config.config import (
    BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT,
    SCREENSHOT_DIR, REPORT_DIR, ALLURE_REPORT_DIR
)


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture
    每个测试函数执行前创建driver，执行后关闭
    """
    # 创建目录
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(ALLURE_REPORT_DIR, exist_ok=True)
    
    # 根据配置创建driver
    browser = BROWSER.lower()
    
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        driver_path = r"D:\WebDriver\chrome\chromedriver.exe"
        service = ChromeService(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument('--headless')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"不支持的浏览器类型: {browser}")
    
    # 设置隐式等待和页面加载超时
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    # 最大化窗口
    driver.maximize_window()
    
    # 将driver附加到allure报告
    allure.attach(
        f"浏览器: {browser}\n无头模式: {HEADLESS}",
        name="测试环境信息",
        attachment_type=allure.attachment_type.TEXT
    )
    
    yield driver
    
    # 测试结束后的清理工作
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest钩子函数，用于获取测试结果
    在测试失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        # 获取测试用例的fixture
        if 'driver' in item.fixturenames:
            driver = item.funcargs['driver']
            
            # 如果测试失败，截图
            if report.failed:
                # 生成截图文件名
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_name = f"{item.name}_{timestamp}_failed.png"
                screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
                
                # 保存截图
                driver.save_screenshot(screenshot_path)
                
                # 添加截图到Allure报告
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # 添加页面源码到报告
                allure.attach(
                    driver.page_source,
                    name="页面HTML源码",
                    attachment_type=allure.attachment_type.HTML
                )


def pytest_collection_modifyitems(config, items):
    """
    修改测试用例的收集
    主要用于设置中文显示
    """
    for item in items:
        # 设置用例名称为中文
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')


# 添加命令行选项
def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="指定浏览器: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="是否使用无头模式"
    )
# # --- 文件顶部的导入语句，这是必须的！ ---
# import pytest
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService

# # --- 你的 fixture 函数 ---

# @pytest.fixture(scope="function")
# def driver(request):
#     """
#     绝对保底方案：使用硬编码的绝对路径来启动 ChromeDriver
#     """
#     # !! 重要：请将下面的路径修改为你电脑上 chromedriver.exe 的真实路径 !!
#     # !! 路径可以使用正斜杠 / 或双反斜杠 \\，但不能用单反斜杠 \ !!
#     driver_path = "D:/WebDriver/chrome/chromedriver.exe"  # <--- 修改这里！

#     print(f"--- 正在初始化 WebDriver (使用硬编码路径: {driver_path}) ---")

#     # 检查文件是否存在，这是一个好习惯
#     if not os.path.exists(driver_path):
#         raise FileNotFoundError(f"致命错误：在指定路径找不到 ChromeDriver: {driver_path}")

#     service = ChromeService(executable_path=driver_path)
#     options = webdriver.ChromeOptions()
#     # 在这里可以添加你需要的 options，比如无头模式
#     # options.add_argument('--headless')
    
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.implicitly_wait(10)
#     driver.maximize_window()

#     yield driver

#     print("--- 测试结束，正在关闭浏览器 ---")
#     driver.quit()

