import json
import random
import re
import string
import time
from logging import Logger
from pathlib import Path
from typing import Any, Literal, NoReturn, Self

import allure
import pytest
from selenium.webdriver import Chrome, Edge, Firefox, Safari
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from library.composer.vd_path import PathVD
from library.model.vd_class import Locator, ValueVD
from library.model.vd_config import ConfigVD
from library.plugin.vd_browser import BrowserVD


class SeleniumVD:
    def __init__(
        self,
        browser_name: str,
        driver: Chrome | Firefox | Edge | Safari,
        method_name: str,
        logger: Logger,
        full_test_name: str,
    ) -> None:
        self.browser_name_instances: dict[str, str] = {}
        self.browser_name_instances["Default"] = browser_name
        self.browser_name: str = self.browser_name_instances["Default"]

        self.driver_instances: dict[str, Chrome | Firefox | Edge | Safari] = {}
        self.driver_instances["Default"] = driver
        self.driver: Chrome | Firefox | Edge | Safari = self.driver_instances["Default"]

        self.logger: Logger = logger
        self.method_name: str = method_name
        self.full_test_name: str = full_test_name
        self.wait_time: int = ValueVD.wait_sec()

        self.log_file_path: PathVD = ""
        self.log_json_full: dict[str, list] = {self.full_test_name: []}
        self.log_json: list = self.log_json_full[self.full_test_name]

        self.failure_screnshot_path: PathVD = ""
        self.failure_screenshot: dict[str, str] = {self.full_test_name: None}

    def get_driver(self) -> Chrome | Firefox | Edge | Safari:
        return self.driver

    def set_driver(
        self, driver: Chrome | Firefox | Edge | Safari
    ) -> Chrome | Firefox | Edge | Safari:
        self.driver = driver
        return self.driver

    def get_browser_name(self) -> str:
        return self.browser_name

    def set_browser_name(self, browser_name: str) -> str:
        self.browser_name = browser_name
        return self.browser_name

    def get_method_name(self) -> str:
        return self.method_name

    def set_method_name(self, method_name: str) -> str:
        self.method_name = method_name
        return self.method_name

    def _append_json_log(self, message: str) -> Self:
        self.log_json.append(message)
        return self

    def log(self, message: str) -> Self:
        self.logger.info(msg=message)
        with allure.step(title=message):
            pass
        return self

    def new_driver_instance(
        self,
        instance_name: str,
        browser_name: str = ConfigVD.Browser.get_default_browser(),
    ) -> Self:
        browser_name = browser_name.title()
        self.driver_instances[instance_name] = BrowserVD.get_browser(
            browser_name=browser_name
        )
        self.browser_name_instances[instance_name] = browser_name
        return self.switch_driver_instance(instance_name=instance_name)

    def switch_driver_instance(self, instance_name: str = "Default") -> Self:
        if instance_name in self.driver_instances:
            self.set_driver(driver=self.driver_instances[instance_name])
            self.set_browser_name(
                browser_name=self.browser_name_instances[instance_name]
            )
            self.log(message=f"Switched to Instance Name - {instance_name}")
        else:
            self.log(message=f"Instance Name - {instance_name} Not Available")
            self.set_driver(driver=self.driver_instances["Default"])
            self.set_browser_name(browser_name=self.browser_name_instances["Default"])
        return self.switch_window(window=self.current_window_handle())

    def sleep(self, seconds: int | float) -> Self:
        time.sleep(seconds)
        return self

    def fullscreen_window(self) -> Self:
        self.get_driver().fullscreen_window()
        return self

    def maximize_window(self) -> Self:
        self.get_driver().maximize_window()
        return self

    def minimize_window(self) -> Self:
        self.get_driver().minimize_window()
        return self

    def delete_all_cookies(self) -> Self:
        self.get_driver().delete_all_cookies()
        return self

    def open(self, url: str) -> Self:
        self.get_driver().get(url=url)
        short_url: str = ConfigVD.URL.find_name_url_list(value=url)
        if not short_url:
            short_url = url.split("//")[1].split(".")[0].lower()
            short_url = (
                short_url.title()
                if "www" not in short_url
                else url.split("//")[1].split(".")[1].title()
            )
        self.log(message=f"\nSetup : {self.browser_name} Opening URL - {short_url}")
        self.maximize_window()
        return self

    def quit(self) -> Self:
        for key, value in self.driver_instances.items():
            if value:
                value.quit()
                self.log(
                    message=f"\nTeardown : {self.browser_name_instances[key]} Closing"
                )
        return self

    def _flush_log_json(self) -> Self:
        with open(file=self.failure_screnshot_path, mode="w") as f:
            json.dump(obj=self.failure_screenshot, fp=f, indent=4)
        return self

    def test_fail(self, failure_message: str) -> NoReturn:
        pytest.fail(failure_message)

    def assert_true(self, condition: bool, failure_message: str = "Assertion") -> Self:
        if not condition:
            self.test_fail(failure_message=failure_message)
        return self

    def assert_false(self, condition: bool, failure_message: str = "Assertion") -> Self:
        if condition:
            self.test_fail(failure_message=failure_message)
        return self

    def title(self) -> str:
        return self.get_driver().title

    def current_url(self) -> str:
        return self.get_driver().current_url

    def page_source(self) -> str:
        return self.get_driver().page_source

    def refresh(self) -> Self:
        self.get_driver().refresh()
        return self

    def back(self) -> Self:
        self.get_driver().back()
        return self

    def forward(self) -> Self:
        self.get_driver().forward()
        return self

    def close(self) -> Self:
        self.get_driver().close()
        return self

    def get_window_size(self) -> dict:
        return self.get_driver().get_window_size()

    def get_window_width(self) -> int:
        return self.get_window_size()["width"]

    def get_window_height(self) -> int:
        return self.get_window_size()["height"]

    def execute_script(self, script: Any, *args: Any) -> Any:
        return self.get_driver().execute_script(script, *args)

    def switch_to(self) -> SwitchTo:
        return self.get_driver().switch_to

    def switch_window(self, window: str) -> Self:
        self.switch_to().window(window_name=window)
        return self

    def current_window_handle(self) -> str:
        return self.get_driver().current_window_handle

    def window_handles(self) -> list[str]:
        return self.get_driver().window_handles

    def switch_other_window(self, index: int | None = None) -> Self:
        current_window: str = self.current_window_handle()
        windows: list[str] = self.window_handles()
        if index is not None and 0 <= index < len(windows):
            self.switch_window(window=windows[index])
        else:
            for window in windows:
                if window != current_window:
                    self.switch_window(window=window)
                    return self
        self.log(message="No Other Window to Switch")
        return self.switch_window(window=self.current_window_handle())

    def switch_frame(self, frame_reference: str | int | WebElement) -> Self:
        self.switch_to().frame(frame_reference=frame_reference)
        return self

    def switch_parent_frame(self) -> Self:
        self.switch_to().parent_frame()
        return self

    def switch_default_content(self) -> Self:
        self.switch_to().default_content()
        return self

    def open_new_tab(self, url: str = "") -> Self:
        self.execute_script(script=f"window.open('{url}');")
        self.switch_window(window=self.window_handles()[-1])
        return self

    def is_present(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> bool:
        for _ in range(wait_seconds + 1):
            if len(self.get_driver().find_elements(*locator)) > 0:
                return True
            else:
                self.sleep(seconds=1)
        return False

    def is_not_present(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> bool:
        for _ in range(wait_seconds + 1):
            if len(self.get_driver().find_elements(*locator)) == 0:
                return True
            else:
                self.sleep(seconds=1)
        return False

    def find_element(
        self,
        locator: Locator,
        wait_seconds: int = ValueVD.wait_sec(),
        failure_message: str = "Element Not Found",
    ) -> WebElement:
        if not self.is_present(locator=locator, wait_seconds=wait_seconds):
            self.test_fail(failure_message=f"{failure_message} - {locator}")
        return self.get_driver().find_elements(*locator)[0]

    def find_elements(
        self,
        locator: Locator,
        wait_seconds: int = ValueVD.wait_sec(),
        failure_message: str = "Element Not Found",
    ) -> list[WebElement]:
        if not self.is_present(locator=locator, wait_seconds=wait_seconds):
            self.test_fail(failure_message=f"{failure_message} - {locator}")
        return self.get_driver().find_elements(*locator)

    def element_location(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> dict[str, int]:
        return self.find_element(locator=locator, wait_seconds=wait_seconds).location

    def keys(self) -> Keys:
        return Keys

    def click(self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()) -> Self:
        self.find_element(locator=locator, wait_seconds=wait_seconds).click()
        return self

    def js_click(self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()) -> Self:
        self.execute_script(
            "arguments[0].click();",
            self.find_element(locator=locator, wait_seconds=wait_seconds),
        )
        return self

    def type(
        self, locator: Locator, type_value: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.find_element(locator=locator, wait_seconds=wait_seconds).send_keys(
            type_value
        )
        return self

    def js_type(
        self, locator: Locator, type_value: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.execute_script(
            "arguments[0].value = arguments[1];",
            self.find_element(locator=locator, wait_seconds=wait_seconds),
            type_value,
        )
        return self

    def clear(self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()) -> Self:
        self.find_element(locator=locator, wait_seconds=wait_seconds).clear()
        return self

    def clear_type(
        self, locator: Locator, type_value: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        return self.clear(locator=locator, wait_seconds=wait_seconds).type(
            locator=locator,
            type_value=type_value,
            wait_seconds=wait_seconds,
        )

    def back_space_clear(
        self,
        locator: Locator,
        back_space_count: int = 100,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> Self:
        return self.type(
            locator=locator,
            type_value=self.keys().BACK_SPACE * back_space_count,
            wait_seconds=wait_seconds,
        )

    def back_space_type(
        self,
        locator: Locator,
        type_value: str,
        back_space_count: int = 100,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> Self:
        return self.back_space_clear(
            locator=locator,
            back_space_count=back_space_count,
            wait_seconds=wait_seconds,
        ).type(
            locator=locator,
            type_value=type_value,
            wait_seconds=wait_seconds,
        )

    def select_dropdown(
        self,
        locator: Locator,
        wait_seconds: int = ValueVD.wait_sec(),
        failure_message: str = "Dropdown Not Found",
    ) -> Select:
        return Select(
            webelement=self.find_element(
                locator=locator,
                wait_seconds=wait_seconds,
                failure_message=failure_message,
            )
        )

    def select_dropdown_by_index(
        self, locator: Locator, index: int, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).select_by_index(index=index)
        return self

    def select_dropdown_by_value(
        self, locator: Locator, value: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).select_by_value(value=value)
        return self

    def select_dropdown_by_visible_text(
        self, locator: Locator, text: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).select_by_visible_text(text=text)
        return self

    def deselect_dropdown_by_index(
        self, locator: Locator, index: int, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).deselect_by_index(index=index)
        return self

    def deselect_dropdown_by_value(
        self, locator: Locator, value: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).deselect_by_value(value=value)
        return self

    def deselect_dropdown_by_visible_text(
        self, locator: Locator, text: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).deselect_by_visible_text(text=text)
        return self

    def all_selected_options(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> list[WebElement]:
        return self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).all_selected_options

    def first_selected_option(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> WebElement:
        return self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).first_selected_option

    def is_select_dropdown_multiple(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> bool | str:
        return self.select_dropdown(
            locator=locator, wait_seconds=wait_seconds
        ).is_multiple

    def select_drodown_options_list_element(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> list[WebElement]:
        return self.select_dropdown(locator=locator, wait_seconds=wait_seconds).options

    def select_drodown_options_list_text(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> list[str]:
        return [
            element.text
            for element in self.select_drodown_options_list_element(
                locator=locator, wait_seconds=wait_seconds
            )
        ]

    def is_displayed(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> bool:
        return self.find_element(
            locator=locator, wait_seconds=wait_seconds
        ).is_displayed()

    def is_enabled(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> bool:
        return self.find_element(
            locator=locator, wait_seconds=wait_seconds
        ).is_enabled()

    def is_selected(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> bool:
        return self.find_element(
            locator=locator, wait_seconds=wait_seconds
        ).is_selected()

    def get_attribute(
        self,
        locator: Locator,
        attribute_name: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> str | None:
        return self.find_element(
            locator=locator, wait_seconds=wait_seconds
        ).get_attribute(name=attribute_name)

    def get_dom_attribute(
        self,
        locator: Locator,
        attribute_name: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> str:
        return self.find_element(
            locator=locator, wait_seconds=wait_seconds
        ).get_dom_attribute(name=attribute_name)

    def change_attribute_value(
        self,
        locator: Locator,
        attribute_name: str,
        type_value: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> Self:
        self.execute_script(
            "arguments[0].setAttribute(arguments[1], arguments[2]);",
            self.find_element(locator=locator, wait_seconds=wait_seconds),
            attribute_name,
            type_value,
        )
        return self

    def delete_attribute(
        self,
        locator: Locator,
        attribute_name: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> Self:
        self.execute_script(
            "arguments[0].removeAttribute(arguments[1]);",
            self.find_element(locator=locator, wait_seconds=wait_seconds),
            attribute_name,
        )
        return self

    def value_of_css_property(
        self,
        locator: Locator,
        property_name: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> str:
        return self.find_element(
            locator=locator, wait_seconds=wait_seconds
        ).value_of_css_property(property_name=property_name)

    def get_text(self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()) -> str:
        return self.find_element(locator=locator, wait_seconds=wait_seconds).text

    def get_text_elements(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> list[str]:
        return [
            ele.text
            for ele in self.find_elements(locator=locator, wait_seconds=wait_seconds)
        ]

    def is_text_in_elements(
        self, locator: Locator, element_text: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> bool:
        return element_text in self.get_text_elements(
            locator=locator, wait_seconds=wait_seconds
        )

    def is_text_contains_in_elements(
        self,
        locator: Locator,
        text_contains: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> bool:
        return any(
            text_contains in element
            for element in self.get_text_elements(
                locator=locator, wait_seconds=wait_seconds
            )
        )

    def find_element_with_text(
        self,
        locator: Locator,
        text_contains: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> WebElement | None:
        for element in self.find_elements(locator=locator, wait_seconds=wait_seconds):
            if text_contains in element.text:
                return element
        return None

    def scroll_into_view(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.execute_script(
            "arguments[0].scrollIntoView(true);",
            self.find_element(locator=locator, wait_seconds=wait_seconds),
        )
        return self

    def scroll_x_y(self, x: int, y: int) -> Self:
        self.execute_script(
            "window.window.scrollTo(arguments[0], arguments[1]);",
            x,
            y,
        )
        return self

    def scroll_element_xy(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        ele_loc: dict[str, int] = self.element_location(
            locator=locator, wait_seconds=wait_seconds
        )
        return self.scroll_x_y(
            x=ele_loc["x"], y=0 if ele_loc["y"] <= 60 else ele_loc["y"] - 60
        )

    def action_chains(self) -> ActionChains:
        return ActionChains(driver=self.get_driver())

    def action_click(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.action_chains().click(
            on_element=self.find_element(locator=locator, wait_seconds=wait_seconds)
        )
        return self

    def action_click_and_hold(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.action_chains().click_and_hold(
            on_element=self.find_element(locator=locator, wait_seconds=wait_seconds)
        )
        return self

    def action_context_click(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.action_chains().context_click(
            on_element=self.find_element(locator=locator, wait_seconds=wait_seconds)
        )
        return self

    def action_double_click(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.action_chains().double_click(
            on_element=self.find_element(locator=locator, wait_seconds=wait_seconds)
        )
        return self

    def action_type(
        self, locator: Locator, type_value: str, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.action_chains().send_keys_to_element(
            self.find_element(locator=locator, wait_seconds=wait_seconds), type_value
        )
        return self

    def action_move_to_element(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.action_chains().move_to_element(
            to_element=self.find_element(locator=locator, wait_seconds=wait_seconds)
        )
        return self

    def action_scroll_to_element(
        self, locator: Locator, wait_seconds: int = ValueVD.wait_sec()
    ) -> Self:
        self.action_chains().scroll_to_element(
            element=self.find_element(locator=locator, wait_seconds=wait_seconds)
        )
        return self

    def action_drag_and_drop(
        self,
        source_locator: Locator,
        target_locator: Locator,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> Self:
        self.action_chains().drag_and_drop(
            source=self.find_element(locator=source_locator, wait_seconds=wait_seconds),
            target=self.find_element(locator=target_locator, wait_seconds=wait_seconds),
        )
        return self

    def get_random_number_between(self, from_: int, to: int) -> int:
        return random.randint(a=from_, b=to)

    def get_random_number(self, length: int) -> int:
        return int("".join(random.choices(population=string.digits, k=length)))

    def get_random_text(self, length: int) -> str:
        return "".join(random.choices(population=string.ascii_letters, k=length))

    def get_random_text_with_number(self, length: int) -> str:
        return "".join(
            random.choices(population=string.ascii_letters + string.digits, k=length)
        )

    def get_number_from_text(self, text: str) -> int:
        numbers: str = re.sub(pattern=r"\D", repl="", string=text)
        return int(numbers) if numbers else 0

    def get_screenshot_as_png(self) -> bytes:
        return self.get_driver().get_screenshot_as_png()

    def get_screenshot_as_base64(self) -> str:
        return self.get_driver().get_screenshot_as_base64()

    def get_base64_html(self) -> str:
        return f'<a href="data:image/png;base64,{self.get_screenshot_as_base64()}"data-featherlight="image"><span class="badge log fail-bg">Screenshot Click Here</span></a>'

    def save_screenshot(self, filename: str | PathVD) -> bool:
        return self.get_driver().save_screenshot(filename=str(object=filename))

    def save_element_screenshot(self, locator: Locator, filename: str | PathVD) -> bool:
        return self.find_element(locator=locator).screenshot(
            filename=str(object=filename)
        )

    def get_element_screenshot_as_png(self, locator: Locator) -> bytes:
        return self.find_element(locator=locator).screenshot_as_png

    def get_path_vd(self) -> PathVD:
        return PathVD

    def is_file_downloaded(
        self,
        file_name_contains: str,
        directory_path: str | PathVD = PathVD.download_path(),
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> PathVD | Literal[False]:
        file_path: Path | Literal[False] = self.get_path_vd().file_name_contains(
            directory_path=directory_path,
            file_name_contains=file_name_contains,
            wait_seconds=wait_seconds,
        )
        if file_path:
            self.log(message=f"Validation : {file_path.name} Present in Directory")
        return file_path

    def delete_file(self, file_path: str | PathVD) -> Self:
        self.get_path_vd().delete_file(file_path=file_path)
        return self

    def _failure_json_html_show(self) -> Self:
        self.failure_screenshot[self.full_test_name] = self.get_base64_html()
        return self

    def allure_attach_screenshot(self, name: str = "Page | Screenshot") -> Self:
        with allure.step(title=name):
            allure.attach(
                self.get_screenshot_as_png(),
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )
            return self

    def allure_attach_element_screenshot(
        self, locator: Locator, name: str = "Element | Screenshot"
    ) -> Self:
        with allure.step(title=name):
            allure.attach(
                self.get_element_screenshot_as_png(locator=locator),
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )
        return self

    def get_string_between(self, text: str, start: str, end: str) -> str:
        try:
            start_index: int = text.index(start) + len(start)
            end_index: int = text.index(end, start_index)
            return text[start_index:end_index]
        except ValueError:
            return ""
