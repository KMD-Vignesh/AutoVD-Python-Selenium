from dataclasses import dataclass
from typing import Literal, Self

from selenium.webdriver.remote.webelement import WebElement

from library.composer.vd_path import PathVD
from library.helper.vd_selenium import SeleniumVD
from library.interface.vd_page import PageVD
from library.model.vd_class import Locator


@dataclass
class SelDevPage(PageVD):
    def __init__(self, selenium: SeleniumVD) -> None:
        super().__init__(selenium=selenium)

    page_header: Locator = Locator.ID(id="bindings")
    latest_version_download_link: Locator = Locator.XPATH(
        xpath="//p[contains(text(),'Latest stable version')]"
    )
    all_download_links: Locator = Locator.XPATH(xpath="//p[@class='card-text']/a")

    def is_sel_dev_page_loaded(self) -> bool:
        is_present: bool = self.selenium.is_present(locator=self.page_header)
        if is_present:
            self.selenium.log(message="Validation : Sel Dev Page Loaded")
        return is_present

    def scroll_to_latest_version(self) -> Self:
        self.selenium.scroll_element_xy(
            locator=self.latest_version_download_link
        ).sleep(seconds=1)
        return self

    def download_link_with_text(self, text_contains: str) -> Self:
        ele_text_list: WebElement | None = self.selenium.find_element_with_text(
            locator=self.all_download_links, text_contains=text_contains
        )
        self.selenium.sleep(seconds=1)
        ele_text_list.click()
        self.selenium.log(
            message=f"Validation : Text - {ele_text_list.text} Present"
        ).sleep(seconds=1)
        return self

    def check_file_download(self, file_name_contains: str) -> Self:
        downloaded_file_path: PathVD | Literal[False] = (
            self.selenium.is_file_downloaded(file_name_contains=file_name_contains)
        )
        self.selenium.assert_true(condition=downloaded_file_path, failure_message="Downloaded File Not in Directory")
        self.selenium.delete_file(file_path=downloaded_file_path).sleep(seconds=2)
        return self
