# AutoVD-Python-Selenium

AutoVD-Python-Selenium is a Python-based automation framework designed for web and API testing. It leverages Selenium WebDriver for browser automation and provides a structured approach to creating page objects and test cases.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Creating a Page Class](#creating-a-page-class)
  - [Writing a Test Case](#writing-a-test-case)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [License](#license)

## Installation

To use AutoVD-Python-Selenium, clone the repository and install the required dependencies:

```bash
git clone https://github.com/KMD-Vignesh/AutoVD-Python-Selenium.git
cd AutoVD-Python-Selenium
pip install -r requirements.txt
```

## Usage

### Creating a Page Class

To create a page class, define a class that inherits from `PageVD` and initialize it with a `SeleniumVD` instance. Use the `Locator` class to define locators for web elements.

```python
from dataclasses import dataclass
from typing import Self

from library.helper.vd_selenium import SeleniumVD
from library.interface.vd_page import PageVD
from library.model.vd_class import Locator

@dataclass
class LoginPage(PageVD):
    def __init__(self, selenium: SeleniumVD) -> None:
        super().__init__(selenium=selenium)

    username_input: Locator = Locator.ID(id="user-name")
    password_input: Locator = Locator.ID(id="password")
    login_button: Locator = Locator.ID(id="login-button")

    def login_to_app(self, username: str, password: str) -> Self:
        self.selenium.type(locator=self.username_input, type_value=username)
        self.selenium.type(locator=self.password_input, type_value=password)
        self.selenium.click(locator=self.login_button)
        self.selenium.log(message="Action : Logged into Application")
        return self
```

### Writing a Test Case

To write a test case, use the `pytest` framework and import your page classes. Initialize the page class with a `SeleniumVD` instance and define your test logic.

```python
import pytest
from pages.sauce_lab.main_page import MainPage

from library.helper.vd_selenium import SeleniumVD
from library.model.vd_config import ConfigVD

@pytest.mark.vignesh
@pytest.mark.add_cart
def test_add_cart_badge_validation(selenium: SeleniumVD) -> None:
    main_page = MainPage(selenium=selenium)
    main_page.open_app(url=ConfigVD.URL.get(key="SauceLab")).login_to_app(
        username=ConfigVD.Credentials.get(key="UserName"),
        password=ConfigVD.Credentials.get(key="Password"),
    ).assert_true(condition=main_page.is_main_page_loaded()).add_cart_product(
        product_name="Sauce Labs Bike Light"
    ).assert_true(condition=main_page.get_product_count_badge() == 1).add_cart_product(
        product_name="Sauce Labs Backpack"
    ).assert_true(condition=main_page.get_product_count_badge() == 2).add_cart_product(
        product_name="Sauce Labs Onesie"
    ).assert_true(condition=main_page.get_product_count_badge() == 3)
```

## Configuration

Configurations such as URLs and credentials are managed through the `vd_config.yml`(setting/config/vd_config.yml). Ensure you have a configuration file

```yaml
Project:
  ProjectName : SauceLab

Pytest:
  IsDryRun : false
  IsFailureRerun : false
  ParallelCount : 5
  IsParallelGroupFile : false
  DeleteConftest : true
  Tag : add_cart

Browser:
  IsHeadless : false
  DefaultBrowser : Chrome
  IsMultiBrowser : false
  DeleteDownloads : true
  MultiBrowserList : 
    - Chrome
    - Firefox
    - Edge
    - Safari

Allure:
  Generate : true
  AutoOpenServer : false

URL:
  SauceLab : https://saucedemo.com
  SelDev : https://www.selenium.dev/downloads/

Credentials:
  UserName : standard_user
  Password : secret_sauce


```

## Running Tests

To run your tests, use the `pytest` command:

```bash
python runner.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
