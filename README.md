# 登录功能Web自动化测试项目

基于 pytest + Selenium + Allure 的登录功能自动化测试框架，采用 Page Object 设计模式和 Excel 数据驱动。

## 📋 项目概述

本项目用于测试登录系统的功能，包括：
- ✅ 正确账号密码登录
- ✅ 错误账号/密码登录验证
- ✅ 空账号/密码验证
- ✅ 错误提示信息验证
- ✅ 错误提示展示时间验证

**测试地址**: https://ldpg.rj.run/admin/signin  
**超级管理员账号**: 513admin  
**密码**: Ld@513.c

## 🏗️ 项目结构

```
login_test/
├── config/                 # 配置文件目录
│   ├── __init__.py
│   └── config.py          # 项目配置
├── pages/                 # Page Object页面对象
│   ├── __init__.py
│   ├── base_page.py      # 页面基类
│   └── login_page.py     # 登录页面
├── tests/                # 测试用例目录
│   ├── __init__.py
│   └── test_login.py     # 登录测试用例
├── utils/                # 工具类目录
│   ├── __init__.py
│   └── excel_reader.py   # Excel读取工具
├── test_data/            # 测试数据目录
│   └── login_test_cases.xlsx  # 测试用例数据
├── reports/              # 测试报告目录
│   ├── allure/          # Allure报告数据
│   ├── html/            # HTML报告
│   └── screenshots/      # 测试截图
├── conftest.py           # pytest配置和fixtures
├── pytest.ini            # pytest配置文件
├── requirements.txt      # 项目依赖
├── generate_test_data.py # 生成测试数据Excel
├── run_tests.py          # 测试执行脚本
├── .gitignore           # Git忽略配置
└── README.md            # 项目说明文档
```

## 📊 Excel测试数据表结构

Excel文件位于 `test_data/login_test_cases.xlsx`，包含以下列：

| 列名 | 说明 | 示例值 |
|------|------|--------|
| case_id | 用例ID，唯一标识 | TC001 |
| case_name | 用例名称 | 正确的账号和密码 |
| username | 测试用的用户名 | 513admin |
| password | 测试用的密码 | Ld@513.c |
| expected | 预期结果 | success / fail |
| description | 用例详细描述 | 使用正确的超级管理员账号和密码登录 |
| run | 是否执行该用例 | yes / no |

### 预期结果说明
- `success`: 预期登录成功
- `fail`: 预期登录失败，显示错误提示

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Chrome/Firefox/Edge 浏览器
- Java 8+ (用于Allure报告)

### 2. 安装依赖

```bash
# 进入项目目录
cd login_test

# 安装Python依赖
pip install -r requirements.txt

# 安装Allure (Windows)
# 下载: https://github.com/allure-framework/allure2/releases
# 解压并添加到系统PATH环境变量
```

### 3. 生成测试数据

```bash
# 生成Excel测试数据文件
python generate_test_data.py
```

这将在 `test_data/` 目录下创建 `login_test_cases.xlsx` 文件，包含10个预定义的测试用例。

### 4. 运行测试

#### 方式1: 使用运行脚本（推荐）

```bash
python run_tests.py
```

然后根据提示选择执行方式：
1. 运行所有测试
2. 运行数据驱动测试（Excel）
3. 运行正向测试
4. 运行异常测试
5. 运行指定用例
6. 仅生成Allure报告

#### 方式2: 使用pytest命令

```bash
# 运行所有测试
pytest

# 运行指定测试类
pytest tests/test_login.py::TestLogin

# 运行指定用例
pytest tests/test_login.py::TestLogin::test_login_with_excel_data

# 使用特定浏览器
pytest --browser=chrome

# 使用无头模式
pytest --headless

# 并行执行(需要安装pytest-xdist)
pytest -n 4
```

### 5. 查看报告

#### Allure报告

```bash
# 生成并打开Allure报告
allure generate reports/allure -o reports/allure-report --clean
allure open reports/allure-report
```

Allure报告包含：
- 测试执行概览
- 测试用例详情
- 失败截图
- 执行时间统计
- 趋势分析

## 🔧 配置说明

### 修改浏览器配置

编辑 `config/config.py`:

```python
# 浏览器配置
BROWSER = 'chrome'  # 支持: chrome, firefox, edge
HEADLESS = False    # 是否无头模式
IMPLICIT_WAIT = 10  # 隐式等待时间(秒)
```

### 修改元素定位器

如果页面元素定位需要调整，编辑 `pages/login_page.py`:

```python
# 方式1: CSS选择器
username_input = (By.CSS_SELECTOR, "input[name='username']")
password_input = (By.CSS_SELECTOR, "input[name='password']")

# 方式2: XPath
username_input = (By.XPATH, "//input[@name='username']")
password_input = (By.XPATH, "//input[@type='password']")
```

**注意**: 项目中提供了多种定位方式示例，请根据实际页面结构选择或修改。

### 添加测试用例

在Excel中添加新行，填写测试数据：

| case_id | case_name | username | password | expected | description | run |
|---------|-----------|----------|----------|----------|-------------|-----|
| TC011 | 新测试用例 | testuser | testpass | fail | 测试描述 | yes |

保存后直接运行测试即可。

## 📝 测试用例说明

### 数据驱动测试 (TestLogin)

从Excel读取测试数据，自动生成参数化测试用例，包括：
- TC001: 正确的账号和密码
- TC002: 错误的账号
- TC003: 错误的密码
- TC004: 账号和密码都错误
- TC005-TC010: 各种边界和异常场景

### 独立测试用例

#### 正向测试 (TestLoginPositive)
- `test_login_with_correct_credentials`: 使用正确凭据登录

#### 异常测试 (TestLoginNegative)
- `test_login_with_wrong_username`: 错误账号
- `test_login_with_wrong_password`: 错误密码
- `test_login_with_empty_username`: 空账号

## 🎯 Page Object设计

### BasePage (基类)
提供通用方法：
- `find_element()`: 查找元素
- `input_text()`: 输入文本
- `click()`: 点击元素
- `get_text()`: 获取文本
- `take_screenshot()`: 截图
- 等等...

### LoginPage (登录页)
登录页面特定方法：
- `open_login_page()`: 打开登录页
- `login()`: 执行登录
- `is_error_message_displayed()`: 检查错误提示
- `verify_error_message()`: 验证错误信息
- `is_login_successful()`: 检查登录状态

## 🔍 元素定位策略

项目支持多种定位方式：

1. **CSS Selector** (推荐)
   ```python
   (By.CSS_SELECTOR, "input[name='username']")
   ```

2. **XPath**
   ```python
   (By.XPATH, "//input[@name='username']")
   ```

3. **ID**
   ```python
   (By.ID, "username")
   ```

4. **Name**
   ```python
   (By.NAME, "username")
   ```

请根据实际页面结构选择最稳定的定位方式。

## 🐛 调试技巧

### 1. 查看元素定位

```python
# 在测试中添加断点或打印
element = login_page.find_element(login_page.username_input)
print(f"元素: {element}")
```

### 2. 查看页面源码

失败时会自动保存到Allure报告中，或手动保存：

```python
with open('page_source.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
```

### 3. 增加等待时间

```python
# 在页面对象中调整
login_page.sleep(5)  # 等待5秒
```

### 4. 禁用无头模式

```python
# config/config.py
HEADLESS = False  # 可以看到浏览器操作过程
```

## 📈 CI/CD集成

### Jenkins示例

```groovy
pipeline {
    agent any
    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --headless'
            }
        }
        stage('Report') {
            steps {
                allure includeProperties: false, 
                       jdk: '', 
                       results: [[path: 'reports/allure']]
            }
        }
    }
}
```

## ❓ 常见问题

### Q1: 元素找不到
**A**: 检查元素定位器是否正确，可能需要根据实际页面调整 `pages/login_page.py` 中的定位器。

### Q2: ChromeDriver版本不匹配
**A**: 项目使用 webdriver-manager 自动管理，如有问题可手动下载对应版本。

### Q3: 测试执行很慢
**A**: 可以使用并行执行: `pytest -n 4` (需要安装 pytest-xdist)

### Q4: Allure报告无法生成
**A**: 确保已安装Java和Allure，并配置了环境变量。

## 📞 联系方式

如有问题或建议，欢迎反馈！

## 📄 许可证

MIT License

---

**祝测试顺利！** 🎉
