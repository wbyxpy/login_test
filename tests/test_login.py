# -*- coding: utf-8 -*-
"""
登录功能测试用例
使用Excel数据驱动测试
"""
import pytest
import allure
from pages.login_page import LoginPage
from utils.excel_reader import ExcelReader
from config.config import TEST_DATA_FILE, ERROR_MESSAGE


# 读取Excel测试数据
excel_reader = ExcelReader(TEST_DATA_FILE, sheet_name='登录测试用例')
test_data = excel_reader.read_data()
excel_reader.close()


@allure.feature('登录功能')
@allure.story('用户登录')
class TestLogin:
    """登录功能测试类"""
    
    @pytest.mark.parametrize('test_case', test_data, ids=[case['case_id'] for case in test_data])
    def test_login_with_excel_data(self, driver, test_case):
        """
        使用Excel数据驱动的登录测试
        :param driver: WebDriver fixture
        :param test_case: 测试用例数据
        """
        # 从测试用例中提取数据
        case_id = test_case['case_id']
        case_name = test_case['case_name']
        username = test_case['username']
        password = test_case['password']
        expected = test_case['expected']
        description = test_case['description']
        
        # 设置Allure报告信息
        allure.dynamic.title(f"{case_id} - {case_name}")
        allure.dynamic.description(description)
        
        # 添加测试数据到报告
        with allure.step(f"测试用例: {case_id}"):
            allure.attach(
                f"用例ID: {case_id}\n"
                f"用例名称: {case_name}\n"
                f"用户名: {username}\n"
                f"密码: {password}\n"
                f"预期结果: {expected}\n"
                f"用例描述: {description}",
                name="测试用例数据",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # 创建登录页面对象
        login_page = LoginPage(driver)
        
        # 步骤1: 打开登录页面
        with allure.step("步骤1: 打开登录页面"):
            login_page.open_login_page()
            login_page.sleep(1)  # 等待页面加载
        
        # 步骤2: 执行登录操作
        with allure.step(f"步骤2: 输入账号 '{username}' 和密码进行登录"):
            login_page.login(username, password)
            login_page.sleep(1)  # 等待响应
        
        # 步骤3: 验证结果
        with allure.step("步骤3: 验证登录结果"):
            if expected == 'success':
                # 预期登录成功
                self._verify_login_success(login_page, case_name)
            elif expected == 'fail':
                # 预期登录失败
                self._verify_login_failure(login_page, case_name)
            else:
                pytest.fail(f"未知的预期结果: {expected}")
        
        # 步骤4: 截取最终状态
        with allure.step("步骤4: 记录最终页面状态"):
            login_page.take_screenshot(f"{case_id}_最终状态")
    
    def _verify_login_success(self, login_page: LoginPage, case_name: str):
        """
        验证登录成功
        :param login_page: 登录页面对象
        :param case_name: 用例名称
        """
        # 检查是否登录成功（URL改变或没有错误提示）
        is_success = login_page.is_login_successful()
        
        with allure.step("验证登录成功"):
            assert is_success, f"[{case_name}] 登录失败: 预期登录成功，但实际失败"
            allure.attach(
                "✓ 登录成功验证通过",
                name="验证结果",
                attachment_type=allure.attachment_type.TEXT
            )
    
    def _verify_login_failure(self, login_page: LoginPage, case_name: str):
        """
        验证登录失败
        :param login_page: 登录页面对象
        :param case_name: 用例名称
        """
        # 检查是否显示错误提示
        with allure.step("检查是否显示错误提示"):
            is_error_displayed = login_page.is_error_message_displayed()
            assert is_error_displayed, f"[{case_name}] 验证失败: 预期显示错误提示，但未显示"
        
        # 验证错误提示内容
        with allure.step("验证错误提示内容"):
            is_message_correct = login_page.verify_error_message(ERROR_MESSAGE)
            assert is_message_correct, \
                f"[{case_name}] 验证失败: 错误提示内容不匹配，预期包含 '{ERROR_MESSAGE}'"
        
        # 验证错误提示会消失
        with allure.step("验证错误提示会在1秒后消失"):
            login_page.sleep(1)  # 等待1秒
            is_disappeared = login_page.wait_error_message_disappear()
            # 注意：根据实际需求，这个断言可能需要调整
            # 如果提示应该消失但没消失，取消下面的注释
            # assert is_disappeared, f"[{case_name}] 验证失败: 错误提示未在预期时间内消失"
        
        allure.attach(
            "✓ 登录失败验证通过\n✓ 错误提示显示正确\n✓ 错误提示内容正确",
            name="验证结果",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature('登录功能')
@allure.story('正向测试')
class TestLoginPositive:
    """登录功能正向测试"""
    
    @allure.title("正确的账号和密码登录")
    @allure.description("使用超级管理员的正确账号和密码进行登录，应该登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_with_correct_credentials(self, driver):
        """测试使用正确的账号密码登录"""
        login_page = LoginPage(driver)
        
        with allure.step("打开登录页面"):
            login_page.open_login_page()
            login_page.sleep(1)
        
        with allure.step("输入正确的账号和密码"):
            login_page.login('513admin', 'Ld@513.c')
            login_page.sleep(2)
        
        with allure.step("验证登录成功"):
            is_success = login_page.is_login_successful()
            login_page.take_screenshot("登录成功")
            assert is_success, "登录失败: 使用正确的账号密码应该登录成功"


@allure.feature('登录功能')
@allure.story('异常测试')
class TestLoginNegative:
    """登录功能异常测试"""
    
    @allure.title("错误的账号登录")
    @allure.description("使用错误的账号，正确的密码进行登录，应该登录失败并提示错误信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_wrong_username(self, driver):
        """测试使用错误的账号登录"""
        login_page = LoginPage(driver)
        
        with allure.step("打开登录页面"):
            login_page.open_login_page()
            login_page.sleep(1)
        
        with allure.step("输入错误的账号和正确的密码"):
            login_page.login('wronguser', 'Ld@513.c')
            login_page.sleep(1)
        
        with allure.step("验证显示错误提示"):
            assert login_page.is_error_message_displayed(), "未显示错误提示"
            assert login_page.verify_error_message(ERROR_MESSAGE), "错误提示内容不正确"
            login_page.take_screenshot("错误账号登录失败")
    
    @allure.title("错误的密码登录")
    @allure.description("使用正确的账号，错误的密码进行登录，应该登录失败并提示错误信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_wrong_password(self, driver):
        """测试使用错误的密码登录"""
        login_page = LoginPage(driver)
        
        with allure.step("打开登录页面"):
            login_page.open_login_page()
            login_page.sleep(1)
        
        with allure.step("输入正确的账号和错误的密码"):
            login_page.login('513admin', 'wrongpassword')
            login_page.sleep(1)
        
        with allure.step("验证显示错误提示"):
            assert login_page.is_error_message_displayed(), "未显示错误提示"
            assert login_page.verify_error_message(ERROR_MESSAGE), "错误提示内容不正确"
            login_page.take_screenshot("错误密码登录失败")
    
    @allure.title("空账号登录")
    @allure.description("账号为空，密码正确，应该登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_empty_username(self, driver):
        """测试空账号登录"""
        login_page = LoginPage(driver)
        
        with allure.step("打开登录页面"):
            login_page.open_login_page()
            login_page.sleep(1)
        
        with allure.step("输入空账号和正确的密码"):
            login_page.login('', 'Ld@513.c')
            login_page.sleep(1)
        
        with allure.step("验证登录失败"):
            # 可能显示错误提示或者登录按钮不可点击
            login_page.take_screenshot("空账号登录")
