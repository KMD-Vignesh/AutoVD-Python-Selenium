<div align="center">

<h1>AutoVD-Python-Selenium</h1>

<p><strong>Layered UI + API test automation framework for Python</strong><br>
Selenium · pytest · Allure · Page Objects · VD Report</p>

<p>
  <a href="https://github.com/KMD-Vignesh/AutoVD-Python-Selenium"><img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12"></a>
  <a href="https://github.com/KMD-Vignesh/AutoVD-Python-Selenium"><img src="https://img.shields.io/badge/Selenium-4.22-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium 4.22"></a>
  <a href="https://github.com/KMD-Vignesh/AutoVD-Python-Selenium"><img src="https://img.shields.io/badge/pytest-8.2-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest 8.2"></a>
  <a href="https://github.com/KMD-Vignesh/AutoVD-Python-Selenium/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-2EA44F?style=for-the-badge" alt="MIT License"></a>
</p>

</div>

<div align="center">

<h3>Vignesh D</h3>

<p><strong>Senior Software Quality Analyst</strong><br>Chennai, India</p>

<p>
  <a href="https://www.linkedin.com/in/kmd-vignesh/"><img src="https://img.shields.io/badge/LinkedIn-Vignesh%20D-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://github.com/KMD-Vignesh"><img src="https://img.shields.io/badge/GitHub-KMD--Vignesh-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</p>

<p>
  <a href="mailto:KMD.Vignesh@outlook.com">KMD.Vignesh@outlook.com</a>
  &nbsp;·&nbsp;
  <a href="mailto:VigneshDhakshnamoorthy@gmail.com">VigneshDhakshnamoorthy@gmail.com</a>
</p>

</div>

## What It Is

A pytest framework that keeps Selenium setup, reporting, and test data out of your tests. A fixture wires the browser, `SeleniumVD` wraps the common actions, and `runner.py` handles cleanup, parallel execution, Allure, and the VD trend report.

- **One command to run** — `python runner.py` reads `vd_config.yml`, builds the pytest command, and writes every report.
- **Chainable page objects** — `PageVD` methods return `self`, so a flow reads as one line.
- **Config-driven runs** — tag, parallel count, browser, and headless mode live in YAML, not code.
- **Two levels of reporting** — Allure for detail, VD Report for the current run plus trends over time.

## Framework Family

Seven implementations of the same layered idea. Pick the stack your team already uses; the concepts and reports stay familiar.

| Framework                       | Stack                         | Covers    | Repository                                                                                  |
| :------------------------------ | :---------------------------- | :-------- | :------------------------------------------------------------------------------------------ |
| **Java + Selenium**             | Java 17 · Selenium 4 · TestNG | UI + REST | [AutoVD-Java-Selenium](https://github.com/KMD-Vignesh/AutoVD-Java-Selenium)                 |
| **Java + Playwright**           | Java 17 · Playwright · TestNG | UI + REST | [AutoVD-Java-Playwright](https://github.com/KMD-Vignesh/AutoVD-Java-Playwright)             |
| **C# + Playwright**             | C# · Playwright · NUnit       | UI        | [AutoVD-CS-Playwright](https://github.com/KMD-Vignesh/AutoVD-CS-Playwright)                 |
| **Python + Selenium** — this repo | Python · Selenium · pytest  | UI + REST | [AutoVD-Python-Selenium](https://github.com/KMD-Vignesh/AutoVD-Python-Selenium)             |
| **Python + Playwright**         | Python · Playwright · pytest  | UI        | [AutoVD-Python-Playwright](https://github.com/KMD-Vignesh/AutoVD-Python-Playwright)         |
| **TypeScript + Playwright**     | TypeScript · Playwright       | UI + REST | [AutoVD-Typescript-Playwright](https://github.com/KMD-Vignesh/AutoVD-Typescript-Playwright) |
| **TypeScript + Cypress**        | TypeScript · Cypress          | UI (E2E)  | [AutoVD-Typescript-Cypress](https://github.com/KMD-Vignesh/AutoVD-Typescript-Cypress)       |

## Quick Start

**Prerequisites:** Python 3.12, pip, Chrome, and the Allure CLI (`Allure.Generate` is on by default).

```bash
git clone https://github.com/KMD-Vignesh/AutoVD-Python-Selenium.git
cd AutoVD-Python-Selenium
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python runner.py
```

On Windows activate with `.venv\Scripts\activate`. Selenium Manager downloads the matching driver on first run.

Open the reports:

```bash
open assets/vd_report/html/vd.html
open assets/allure/html/index.html
```

On Linux use `xdg-open`; on Windows open the files from Explorer.

## Configuration

Everything runtime lives in `setting/config/vd_config.yml`.

```yaml
Pytest:
  Tag : add_cart
  ParallelCount : 5
Browser:
  IsHeadless : false
  DefaultBrowser : Chrome
```

| Key | Default | What it does |
| :--- | :--- | :--- |
| `Pytest.Tag` | `add_cart` | pytest marker to run; leave empty to run everything |
| `Pytest.ParallelCount` | `5` | `pytest-xdist` worker count |
| `Pytest.IsDryRun` | `false` | Collect tests without running them |
| `Pytest.IsFailureRerun` | `false` | Rerun only the failures from the last run |
| `Browser.IsHeadless` | `false` | Run without a visible window |
| `Browser.DefaultBrowser` | `Chrome` | Chrome, Firefox, Edge, or Safari |
| `Browser.IsMultiBrowser` | `false` | Run each test once per browser in `MultiBrowserList` |
| `Allure.Generate` | `true` | Build the Allure HTML report |
| `URL.*` / `Credentials.*` | SauceDemo values | Base URLs and login data used by tests |

Test markers are declared in `pytest.ini`: `vignesh`, `add_cart`, `remove_cart`, `sel_dev`.

## Writing Tests

A page object extends `PageVD` and declares `Locator` fields:

```python
from dataclasses import dataclass
from typing import Self

from library.helper.vd_selenium import SeleniumVD
from library.interface.vd_page import PageVD
from library.model.vd_class import Locator


@dataclass
class LoginPage(PageVD):
    username_input: Locator = Locator.ID(id="user-name")
    password_input: Locator = Locator.ID(id="password")
    login_button: Locator = Locator.ID(id="login-button")

    def login_to_app(self, username: str, password: str) -> Self:
        self.selenium.type(locator=self.username_input, type_value=username)
        self.selenium.type(locator=self.password_input, type_value=password)
        self.selenium.click(locator=self.login_button)
        return self
```

A test takes the generated `selenium` fixture and chains the page:

```python
import pytest
from pages.sauce_lab.main_page import MainPage
from library.helper.vd_selenium import SeleniumVD
from library.model.vd_config import ConfigVD


@pytest.mark.add_cart
def test_add_cart_badge_validation(selenium: SeleniumVD) -> None:
    main_page = MainPage(selenium=selenium)
    main_page.open_app(url=ConfigVD.URL.get(key="SauceLab")).login_to_app(
        username=ConfigVD.Credentials.get(key="UserName"),
        password=ConfigVD.Credentials.get(key="Password"),
    ).assert_true(condition=main_page.is_main_page_loaded()).add_cart_product(
        product_name="Sauce Labs Bike Light"
    ).assert_true(condition=main_page.get_product_count_badge() == 1)
```

The `selenium` fixture is defined in `library/interface/vd_base.py`; `runner.py` generates a one-line `conftest.py` that exposes it, then removes it after the run (`DeleteConftest`).

## Framework Map

Read these in order. Everything else supports them.

| Package | Key classes | What it does |
| :--- | :--- | :--- |
| `library/interface` | `vd_base.py`, `PageVD` | Browser fixture, pytest hooks, page-object base. **Start here.** |
| `library/composer` | `RunnerVD`, `PathVD` | Builds the pytest command, cleans artifacts, resolves every path |
| `library/helper` | `SeleniumVD`, `ApiVD` | Browser actions and REST calls |
| `library/model` | `ConfigVD`, `Locator`, `ValueVD` | Config access and locator types |
| `library/plugin` | `BrowserVD`, `ReportVD` | Driver lifecycle and VD report generation |
| `src/pages` | `LoginPage`, `MainPage`, `SelDevPage` | Page objects |
| `src/tests` | `add_cart.py`, `remove_cart.py`, `sel_dev.py` | Tests |
| `setting/config` | `vd_config.yml` | Runtime settings |

A few things carry most of the work:

| Item | Use |
| :--- | :--- |
| `SeleniumVD.open(url)` | Navigate |
| `SeleniumVD.type/click/get_text` | Interact with a `Locator` |
| `SeleniumVD.assert_true(...)` | Assert and report in one step |
| `SeleniumVD.log(...)` | Add a step to the report |
| `ConfigVD.URL.get(key=...)` | Read a URL or credential from YAML |
| `PageVD` | Base class for page objects |

## How a Run Works

1. `runner.py` creates the temporary `conftest.py` and cleans old downloads and reports.
2. It builds the pytest command from `vd_config.yml`: tag, parallel workers, Allure, HTML, JSON, and JUnit XML.
3. pytest runs the tagged tests; the fixture starts and stops a browser per test.
4. Allure generates its HTML report; the temporary conftest and caches are removed.
5. `ReportVD` writes `vd.html`, `trend.html`, and their JSON files to `assets/vd_report/`.

## Project Layout

```text
AutoVD-Python-Selenium/
├── runner.py                    # entry point: python runner.py
├── pytest.ini                   # markers and test paths
├── requirements.txt             # pinned dependencies
├── setting/config/vd_config.yml # runtime configuration
├── library/                     # framework: composer, helper, interface, model, plugin
├── src/pages/                   # page objects
├── src/tests/                   # tests
└── assets/                      # generated: VD report, Allure, pytest, downloads
```

`assets/` is generated output and is recreated by the runner.

## Reports

| Output | Location |
| :--- | :--- |
| VD current report | `assets/vd_report/html/vd.html` |
| VD trend report | `assets/vd_report/html/trend.html` |
| VD data / failures | `assets/vd_report/json/` |
| Failure screenshots | `assets/vd_report/screenshot/` |
| Allure HTML | `assets/allure/html/index.html` |
| pytest HTML | `assets/pytest/html/pytest.html` |
| pytest JSON / XML | `assets/pytest/json/pytest.json`, `assets/pytest/xml/pytest.xml` |

The trend report keeps history, so you can compare runs by date and time.

## Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| No tests run | Check `Pytest.Tag`; it must match a marker in `pytest.ini`. Leave it empty to run all. |
| `allure: command not found` | Install the Allure CLI, or set `Allure.Generate: false`. |
| Browser does not start | Install Chrome/Firefox, or switch `DefaultBrowser`. Selenium Manager fetches the driver. |
| Tests run with a visible browser in CI | Set `Browser.IsHeadless: true`. |
| `conftest.py` is missing | It is generated per run by `runner.py`; use the runner, not bare `pytest`. |
| Old screenshots or downloads remain | The runner cleans downloads and report folders at the start; check `DeleteDownloads`. |

## License

MIT. See [`LICENSE`](LICENSE).
