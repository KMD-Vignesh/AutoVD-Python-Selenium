from dataclasses import dataclass
from typing import Self

from pages.sauce_lab.login_page import LoginPage

from library.helper.vd_selenium import SeleniumVD
from library.model.vd_class import Locator


@dataclass
class MainPage(LoginPage):
    def __init__(self, selenium: SeleniumVD) -> None:
        super().__init__(selenium=selenium)

    main_page_header: Locator = Locator.XPATH(
        xpath="//div[@class='header_label']/div[text()='Swag Labs']"
    )
    product_count_xpath: Locator = Locator.XPATH(
        xpath="//span[@class='shopping_cart_badge']"
    )

    def is_main_page_loaded(self) -> bool:
        is_present: bool = self.selenium.is_present(locator=self.main_page_header)
        if is_present:
            self.selenium.log(message="Validation : Main Page Loaded")
            self.selenium.allure_attach_screenshot()
        return is_present

    def add_cart_product(self, product_name: str) -> Self:
        product_xpath: Locator = Locator.XPATH(
            xpath=f"//div[text()='{product_name}']/../../..//button"
        )
        self.selenium.scroll_element_xy(locator=product_xpath).sleep(seconds=1)
        self.selenium.click(locator=product_xpath).sleep(seconds=1)
        self.selenium.log(message=f"Action : {product_name} Added To Cart")
        return self

    def get_product_count_badge(self) -> int:
        product_count: int = int(
            self.selenium.get_text(locator=self.product_count_xpath)
        )
        self.selenium.scroll_element_xy(locator=self.main_page_header).sleep(seconds=1)
        self.selenium.allure_attach_element_screenshot(locator=self.product_count_xpath)
        self.selenium.log(
            message=f"Validation : Shopping Cart Badge Count = {product_count}"
        )
        return product_count
