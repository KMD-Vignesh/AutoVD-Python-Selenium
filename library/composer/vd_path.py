import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Literal

from library.model.vd_class import ValueVD


class PathVD(Path):
    """ROOT"""

    @staticmethod
    def project_path() -> "PathVD":
        return PathVD(__file__).resolve().parents[2]

    """SUB ROOT"""

    @staticmethod
    def assets_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.project_path() / "assets")

    @staticmethod
    def setting_path() -> "PathVD":
        return PathVD.project_path() / "setting"

    @staticmethod
    def library_path() -> "PathVD":
        return PathVD.project_path() / "library"

    @staticmethod
    def src_path() -> "PathVD":
        return PathVD.project_path() / "src"

    @staticmethod
    def src_pages_path() -> "PathVD":
        return PathVD.src_path() / "pages"

    @staticmethod
    def src_tests_path() -> "PathVD":
        return PathVD.src_path() / "tests"

    @staticmethod
    def conftest_file_path() -> "PathVD":
        return PathVD.src_tests_path() / "conftest.py"

    """ ASSET SUB ROOT """

    """ ALLURE """

    @staticmethod
    def allure_path() -> "PathVD":
        return PathVD.assets_path() / "allure"

    @staticmethod
    def allure_html_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.allure_path() / "html")

    @staticmethod
    def allure_logs_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.allure_path() / "logs")

    @staticmethod
    def allure_html_history_path() -> "PathVD":
        return PathVD.create_directory(
            directory_path=PathVD.allure_html_path() / "history"
        )

    @staticmethod
    def allure_logs_history_path() -> "PathVD":
        return PathVD.create_directory(
            directory_path=PathVD.allure_logs_path() / "history"
        )

    @staticmethod
    def allure_html_data_path() -> "PathVD":
        return PathVD.create_directory(
            directory_path=PathVD.allure_html_path() / "data"
        )

    @staticmethod
    def allure_html_data_tc_path() -> "PathVD":
        return PathVD.create_directory(
            directory_path=PathVD.allure_html_data_path() / "test-cases"
        )

    @staticmethod
    def allure_suites_csv_path() -> "PathVD":
        return PathVD.create_directory(
            directory_path=PathVD.allure_html_data_tc_path() / "suites.csv"
        )

    """ DOWNLOAD """

    @staticmethod
    def download_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.assets_path() / "download")

    """ PYTEST """

    @staticmethod
    def pytest_path() -> "PathVD":
        return PathVD.assets_path() / "pytest"

    @staticmethod
    def pytest_html_path() -> "PathVD":
        return PathVD.pytest_path() / "html"

    @staticmethod
    def pytest_json_path() -> "PathVD":
        return PathVD.pytest_path() / "json"

    @staticmethod
    def pytest_xml_path() -> "PathVD":
        return PathVD.pytest_path() / "xml"

    @staticmethod
    def pytest_doc_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.pytest_path() / "doc")

    @staticmethod
    def pytest_dry_run_file_path() -> "PathVD":
        return PathVD.pytest_doc_path() / "dry_run.txt"

    """ VD Report """

    @staticmethod
    def vd_report_path() -> "PathVD":
        return PathVD.assets_path() / "vd_report"

    @staticmethod
    def vd_report_html_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.vd_report_path() / "html")

    @staticmethod
    def vd_report_json_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.vd_report_path() / "json")

    @staticmethod
    def vd_report_logs_path() -> "PathVD":
        return PathVD.create_directory(directory_path=PathVD.vd_report_path() / "logs")

    @staticmethod
    def vd_source_path() -> "PathVD":
        return PathVD.library_path() / "source"

    @staticmethod
    def vd_html_file_path() -> "PathVD":
        return PathVD.create_file(file_path=PathVD.vd_report_html_path() / "vd.html")

    @staticmethod
    def vd_json_file_path() -> "PathVD":
        return PathVD.create_file(file_path=PathVD.vd_report_json_path() / "vd.json")

    @staticmethod
    def trend_html_file_path() -> "PathVD":
        return PathVD.create_file(file_path=PathVD.vd_report_html_path() / "trend.html")

    @staticmethod
    def trend_json_file_path() -> "PathVD":
        return PathVD.create_file(file_path=PathVD.vd_report_json_path() / "trend.json")

    @staticmethod
    def vd_css_file_path() -> "PathVD":
        return PathVD.create_file(file_path=PathVD.vd_source_path() / "vd.css")

    @staticmethod
    def vd_js_file_path() -> "PathVD":
        return PathVD.create_file(file_path=PathVD.vd_source_path() / "vd.js")

    @staticmethod
    def failure_json_file_path() -> "PathVD":
        return PathVD.vd_report_json_path() / "failure.json"

    @staticmethod
    def failure_screenshot_path() -> "PathVD":
        return PathVD.create_directory(
            directory_path=PathVD.vd_report_path() / "screenshot"
        )

    @staticmethod
    def failure_timestamp_png_path(name: str) -> "PathVD":
        d_time: str = f"{name}_{datetime.now().strftime(format="%d_%m_%y_%H_%M_%S")}"
        return PathVD.failure_screenshot_path() / f"{d_time}.png"

    """ SETTING SUB ROOT """

    """ CONFIG """

    @staticmethod
    def setting_config_path() -> "PathVD":
        return PathVD.setting_path() / "config"

    @staticmethod
    def vd_config_file_path() -> "PathVD":
        return PathVD.setting_config_path() / "vd_config.yml"

    """ DATA """

    @staticmethod
    def setting_data_path() -> "PathVD":
        return PathVD.setting_path() / "data"

    """ FILEDIR HELPER """

    @staticmethod
    def create_file(file_path: str | Path) -> "PathVD":
        path: Path = PathVD(file_path)
        if not path.exists():
            path.touch()
        return path

    @staticmethod
    def delete_file(file_path: str | Path) -> None:
        path: Path = PathVD(file_path)
        if path.exists():
            path.unlink()

    @staticmethod
    def create_directory(directory_path: str | Path) -> "PathVD":
        path: Path = PathVD(directory_path)
        if not path.exists():
            path.mkdir(parents=True)
        return path

    @staticmethod
    def delete_directory(directory_path: str | Path) -> None:
        path: Path = PathVD(directory_path)
        if path.exists() and path.is_dir():
            shutil.rmtree(path)

    @staticmethod
    def file_name_contains(
        directory_path: str | Path,
        file_name_contains: str,
        wait_seconds: int = ValueVD.wait_sec(),
    ) -> Path | Literal[False]:
        path: Path = Path(directory_path)
        for _ in range(wait_seconds):
            for file in path.iterdir():
                if file.is_file() and file_name_contains in file.name:
                    return file
                else:
                    time.sleep(1)
        return False

    @staticmethod
    def move_file(source: str | Path, target: str | Path) -> None:
        src_path: Path = Path(source)
        dst_path: Path = Path(target)
        if src_path.exists() and src_path.is_file():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            if dst_path.exists():
                dst_path.unlink()
            src_path.rename(target=dst_path)

    @staticmethod
    def move_directory(source: str | Path, target: str | Path) -> None:
        src_path: Path = Path(source)
        dst_path: Path = Path(target)
        if src_path.exists() and src_path.is_dir():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            if dst_path.exists() and dst_path.is_dir():
                shutil.rmtree(dst_path)
            src_path.rename(target=dst_path)

    @staticmethod
    def remove_directory(folder_path: str | Path, name_contains: str):
        folder = Path(folder_path)
        for pycache in folder.rglob(pattern=name_contains):
            try:
                if ".venv" not in str(pycache):
                    shutil.rmtree(pycache)
            except OSError as e:
                print(f"Error: {e}")
