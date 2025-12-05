# -*- coding: utf-8 -*-
"""
登录页面对象
"""
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import LOGIN_URL, ERROR_MESSAGE_DISPLAY_TIME


class LoginPage(BasePage):
    """登录页面类"""
    
    # 页面元素定位器
    # 注意：以下定位器是示例，需要根据实际页面调整
    # 这里提供了多种常见的定位方式供选择
    
    # 方式1: 使用CSS选择器
    username_input = (By.CSS_SELECTOR, '#identifier')
    #password_input = (By.CSS_SELECTOR, "input[name='password']")
    login_button = (By.CSS_SELECTOR, "button[type='submit'].bg-gradient-to-r.text-white")
    #error_message = (By.CSS_SELECTOR, ".error-message, .alert-danger, .message-error")
    
    # 方式2: 使用XPath（备选方案）
    # username_input = (By.XPATH, "/html/body/div/div[1]/div[2]/div/div/form/div[2]/input")
    password_input = (By.XPATH, '//*[@id="password"]')
    #login_button = (By.XPATH, "/html/body/div[2]/div/div[2]/form/button")
    # error_message = (By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'alert')]")
    
    # 方式3: 更通用的XPath定位
    # username_input = (By.XPATH, "//input[contains(@placeholder, '账号') or contains(@placeholder, '用户名')]")
    # password_input = (By.XPATH, "//input[@type='password']")
    # login_button = (By.XPATH, "//button[contains(., '登录')] | //input[@type='submit']")
    
    def __init__(self, driver):
        """
        初始化登录页面
        :param driver: WebDriver实例
        """
        super().__init__(driver)
    
    @allure.step("打开登录页面")
    def open_login_page(self):
        """打开登录页面"""
        self.open(LOGIN_URL)
        allure.attach(LOGIN_URL, name="登录页面URL", attachment_type=allure.attachment_type.TEXT)
    
    @allure.step("输入用户名: {username}")
    def input_username(self, username: str):
        """
        输入用户名
        :param username: 用户名
        """
        self.input_text(self.username_input, username)
    
    @allure.step("输入密码: {password}")
    def input_password(self, password: str):
        """
        输入密码（在allure报告中显示，但实际项目可考虑脱敏）
        :param password: 密码
        """
        # 注意：实际生产环境建议对密码进行脱敏处理
        self.input_text(self.password_input, password)
    
    @allure.step("点击登录按钮")
    def click_login_button(self):
        """点击登录按钮"""
        self.click(self.login_button)
    
    @allure.step("执行登录操作")
    def login(self, username: str, password: str):
        """
        执行完整的登录操作
        :param username: 用户名
        :param password: 密码
        """
        self.input_username(username)
        self.input_password(password)
        self.take_screenshot("登录前截图")
        self.click_login_button()
        # 等待页面响应
        self.sleep(0.5)
    
    @allure.step("检查错误提示是否显示")
    def is_error_message_displayed(self) -> bool:
        """
        检查错误提示是否显示
        :return: True表示显示，False表示不显示
        """
        return self.is_element_present(self.error_message, timeout=2)
    
    @allure.step("获取错误提示信息")
    def get_error_message_text(self) -> str:
        """
        获取错误提示信息文本
        :return: 错误提示文本
        """
        if self.is_error_message_displayed():
            text = self.get_text(self.error_message)
            allure.attach(text, name="错误提示信息", attachment_type=allure.attachment_type.TEXT)
            return text
        return ""
    
    @allure.step("等待错误提示消失")
    def wait_error_message_disappear(self) -> bool:
        """
        等待错误提示消失
        :return: True表示已消失，False表示超时仍显示
        """
        # 等待提示消失，超时时间设置为提示展示时间+2秒
        timeout = ERROR_MESSAGE_DISPLAY_TIME + 2
        return self.wait_element_disappear(self.error_message, timeout=timeout)
    
    @allure.step("检查是否登录成功")
    def is_login_successful(self) -> bool:
        """
        检查是否登录成功
        通过URL变化或页面元素判断
        :return: True表示登录成功
        """
        self.sleep(1)  # 等待页面跳转
        current_url = self.get_current_url()
        
        # 登录成功后URL应该不再是登录页面
        # 这里假设登录成功后会跳转到其他页面
        is_success = LOGIN_URL not in current_url or current_url != LOGIN_URL
        
        # 或者也可以检查是否还在登录页面且没有错误提示
        # is_success = not self.is_error_message_displayed()
        
        allure.attach(
            f"当前URL: {current_url}\n登录成功: {is_success}",
            name="登录结果检查",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return is_success
    
    @allure.step("验证错误提示内容是否正确")
    def verify_error_message(self, expected_message: str) -> bool:
        """
        验证错误提示内容
        :param expected_message: 期望的错误提示信息
        :return: True表示匹配
        """
        actual_message = self.get_error_message_text()
        is_match = expected_message in actual_message
        
        allure.attach(
            f"期望提示: {expected_message}\n实际提示: {actual_message}\n是否匹配: {is_match}",
            name="错误提示验证",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return is_match
