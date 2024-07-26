import sys

from library.composer.vd_path import PathVD

sys.path.append(".")
sys.path.append("src")
import logging
from typing import Any, Generator

import allure
import pytest
from pytest_metadata.plugin import metadata_key

from library.helper.vd_selenium import SeleniumVD
from library.model.vd_config import ConfigVD
from library.plugin.vd_browser import BrowserVD

logging.basicConfig(level=logging.INFO, format="\n%(message)s", stream=sys.stderr)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> Generator[None, Any, None]:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_html_report_title(report):
    report.title = f"Test Report - {ConfigVD.Project.get_project_name()}"


def pytest_configure(config):
    config.stash[metadata_key].pop("Packages")
    config.stash[metadata_key].pop("Plugins")


def get_browser_list() -> list[str]:
    if ConfigVD.Browser.is_multi_browser():
        return ConfigVD.Browser.get_multi_browser_list()
    else:
        return [ConfigVD.Browser.get_default_browser()]


@allure.title(test_title="Setup / Teardown")
@pytest.fixture(params=get_browser_list())
def selenium(request: pytest.FixtureRequest) -> SeleniumVD:  # type: ignore
    file_path: str = (
        f"src/tests/{str(object=PathVD(request.node.fspath)).split('src/tests/')[1]}"
    )
    browser_name = request.param
    method_name: str = request.node.name
    full_test_name: str = f"{file_path}::{method_name}"
    logger: logging.Logger = logging.getLogger(name=method_name)
    if logger.hasHandlers():
        logger.handlers.clear()
    formatter = logging.Formatter(fmt="%(message)s")
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(fmt=formatter)
    logger.addHandler(hdlr=handler)
    logger.propagate = False
    selenium: SeleniumVD = SeleniumVD(
        browser_name=browser_name.title(),
        driver=BrowserVD.get_browser(browser_name=browser_name),
        method_name=method_name,
        logger=logger,
        full_test_name=full_test_name,
    )
    yield selenium
    if request.node.rep_call.failed:
        # reason: str = (
        #     request.node.rep_call.longrepr
        #     if request.node.rep_call.longrepr
        #     else "Unknown reason"
        # )
        # selenium._append_json_log(message=f"Error : {reason}")
        try:
            selenium.allure_attach_screenshot(name="Page | Screenshot")
        except Exception:
            pass
    selenium.quit()
