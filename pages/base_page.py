# -*- coding: utf-8 -*-
"""
页面基类
"""
import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple


class BasePage:
    """页面基类，封装常用操作"""
    
    def __init__(self, driver):
        """
        初始化页面对象
        :param driver: WebDriver实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        try:
            self.driver.maximize_window()
        except Exception:
            pass
    
    @allure.step("打开页面: {url}")
    def open(self, url: str):
        """
        打开指定URL
        :param url: 页面URL
        """
        self.driver.get(url)
    
    @allure.step("查找元素: {locator}")
    def find_element(self, locator: Tuple[str, str], timeout: int = 10):
        """
        查找单个元素
        :param locator: 定位器元组 (By.XXX, value)
        :param timeout: 超时时间
        :return: WebElement
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"元素查找失败_{locator}",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"超时: 无法找到元素 {locator}")
    
    @allure.step("查找多个元素: {locator}")
    def find_elements(self, locator: Tuple[str, str], timeout: int = 10):
        """
        查找多个元素
        :param locator: 定位器元组
        :param timeout: 超时时间
        :return: WebElement列表
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"元素查找失败_{locator}",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"超时: 无法找到元素 {locator}")
    
    @allure.step("输入文本: {text}")
    def input_text(self, locator: Tuple[str, str], text: str):
        """
        输入文本到元素
        :param locator: 定位器
        :param text: 输入的文本
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("点击元素")
    def click(self, locator: Tuple[str, str]):
        """
        点击元素
        :param locator: 定位器
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    @allure.step("获取元素文本")
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        获取元素文本
        :param locator: 定位器
        :return: 元素文本
        """
        element = self.find_element(locator)
        return element.text
    
    @allure.step("检查元素是否存在")
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 3) -> bool:
        """
        检查元素是否存在
        :param locator: 定位器
        :param timeout: 超时时间
        :return: True/False
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @allure.step("等待元素消失")
    def wait_element_disappear(self, locator: Tuple[str, str], timeout: int = 10) -> bool:
        """
        等待元素消失
        :param locator: 定位器
        :param timeout: 超时时间
        :return: True/False
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    @allure.step("获取当前URL")
    def get_current_url(self) -> str:
        """
        获取当前页面URL
        :return: 当前URL
        """
        return self.driver.current_url
    
    @allure.step("获取页面标题")
    def get_title(self) -> str:
        """
        获取页面标题
        :return: 页面标题
        """
        return self.driver.title
    
    @allure.step("截图")
    def take_screenshot(self, name: str = "screenshot"):
        """
        截取当前页面截图并添加到Allure报告
        :param name: 截图名称
        """
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    
    def sleep(self, seconds: int):
        """
        等待指定秒数
        :param seconds: 等待秒数
        """
        time.sleep(seconds)
