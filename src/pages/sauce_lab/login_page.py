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
