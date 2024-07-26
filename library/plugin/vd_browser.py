from selenium.webdriver import Chrome, Edge, Firefox, Safari
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService

from library.composer.vd_path import PathVD
from library.model.vd_config import ConfigVD


class BrowserVD:
    @staticmethod
    def get_browser(
        browser_name: str,
        headless: bool = ConfigVD.Browser.is_headless(),
    ) -> Chrome | Firefox | Edge | Safari:
        download_path: PathVD = PathVD.download_path()
        download_dir = str(object=download_path)
        match browser_name.lower():
            case "chrome":
                chrome_options = ChromeOptions()
                if headless:
                    chrome_options.add_argument(argument="--headless")
                chrome_prefs: dict[str, str] = {
                    "download.default_directory": download_dir
                }
                chrome_options.add_experimental_option(name="prefs", value=chrome_prefs)
                return Chrome(service=ChromeService(), options=chrome_options)
            case "firefox":
                firefox_options = FirefoxOptions()
                if headless:
                    firefox_options.add_argument(argument="--headless")
                firefox_options.set_preference(
                    name="browser.download.folderList", value=2
                )
                firefox_options.set_preference(
                    name="browser.download.dir", value=download_dir
                )
                firefox_options.set_preference(
                    name="browser.helperApps.neverAsk.saveToDisk",
                    value="application/pdf",
                )
                return Firefox(service=FirefoxService(), options=firefox_options)
            case "edge":
                edge_options = EdgeOptions()
                if headless:
                    edge_options.add_argument(argument="--headless")
                edge_prefs: dict[str, str] = {
                    "download.default_directory": download_dir
                }
                edge_options.add_experimental_option(name="prefs", value=edge_prefs)
                return Edge(service=EdgeService(), options=edge_options)
            case "safari":
                safari_options = SafariOptions()
                if headless:
                    print("Safari does not support headless mode.")
                print(
                    "Note: Setting download directory is not supported by Safari WebDriver."
                )
                return Safari(service=SafariService(), options=safari_options)
            case _:
                raise ValueError(f"Unsupported browser: {browser_name}")
