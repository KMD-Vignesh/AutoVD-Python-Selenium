from selenium.webdriver.common.by import By


class ValueVD:
    @staticmethod
    def wait_sec() -> int:
        return 15

    @staticmethod
    def bold(message: str) -> str:
        return f"\033[1m{message}\033[0m"

    @staticmethod
    def color_red(message: str) -> str:
        return f"\033[91m{message}\033[0m"

    @staticmethod
    def color_blue(message: str) -> str:
        return f"\033[94m{message}\033[0m"

    @staticmethod
    def color_yellow(message: str) -> str:
        return f"\033[93m{message}\033[0m"

    @staticmethod
    def color_green(message: str) -> str:
        return f"\033[92m{message}\033[0m"

    @staticmethod
    def color_cyan(message: str) -> str:
        return f"\033[96m{message}\033[0m"

    @staticmethod
    def color_magenta(message: str) -> str:
        return f"\033[95m{message}\033[0m"

    @staticmethod
    def test_result_d_t_format() -> str:
        return "%d/%m/%y %H:%M:%S"


class Locator:
    @staticmethod
    def CLASS_NAME(class_name: str) -> "Locator":
        return (By.CLASS_NAME, class_name)

    @staticmethod
    def CSS_SELECTOR(css_selector: str) -> "Locator":
        return (By.CSS_SELECTOR, css_selector)

    @staticmethod
    def ID(id: str) -> "Locator":
        return (By.ID, id)

    @staticmethod
    def LINK_TEXT(link_text: str) -> "Locator":
        return (By.LINK_TEXT, link_text)

    @staticmethod
    def NAME(name: str) -> "Locator":
        return (By.NAME, name)

    @staticmethod
    def PARTIAL_LINK_TEXT(link_text_contains: str) -> "Locator":
        return (By.PARTIAL_LINK_TEXT, link_text_contains)

    @staticmethod
    def TAG_NAME(tag_name: str) -> "Locator":
        return (By.TAG_NAME, tag_name)

    @staticmethod
    def XPATH(xpath: str) -> "Locator":
        return (By.XPATH, xpath)
