from dataclasses import dataclass
from typing import Self

from library.helper.vd_selenium import SeleniumVD


@dataclass
class PageVD:
    def __init__(self, selenium: SeleniumVD) -> None:
        self.selenium: SeleniumVD = selenium

    def open_app(self, url: str) -> Self:
        self.selenium.open(url=url)
        return self

    def log(self, message: str) -> Self:
        self.selenium.log(message=message)
        return self

    def sleep(self, seconds: int | float) -> Self:
        self.selenium.sleep(seconds=seconds)
        return self

    def assert_true(self, condition: bool, failure_message: str = "Assertion") -> Self:
        self.selenium.assert_true(condition=condition, failure_message=failure_message)
        return self

    def assert_false(self, condition: bool, failure_message: str = "Assertion") -> Self:
        self.selenium.assert_false(condition=condition, failure_message=failure_message)
        return self
