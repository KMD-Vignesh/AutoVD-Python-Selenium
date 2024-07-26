import json
import re
import sys
import time

from library.model.vd_config import ConfigVD

sys.path.append(".")
sys.path.append("src")
import subprocess
from datetime import datetime, timedelta

from library.composer.vd_path import PathVD
from library.model.vd_class import ValueVD
from library.plugin.vd_report import ReportVD


class RunnerVD:
    @staticmethod
    def _pre_cleanup() -> None:
        if ConfigVD.Browser.is_delete_downloads():
            PathVD.delete_directory(directory_path=PathVD.download_path())
        PathVD.delete_directory(directory_path=PathVD.allure_logs_path())
        PathVD.delete_directory(directory_path=PathVD.failure_screenshot_path())
        PathVD.move_directory(
            source=PathVD.allure_html_history_path(),
            target=PathVD.allure_logs_history_path(),
        )
        PathVD.delete_directory(directory_path=PathVD.allure_html_path())
        PathVD.delete_directory(directory_path=PathVD.vd_report_logs_path())
        PathVD.download_path()
    
    @staticmethod
    def _auto_conftest_file() -> None:
        if not PathVD.conftest_file_path().exists():
            multiline_string = 'import sys\nsys.path.append(".")\nfrom library.interface.vd_base import *  # noqa: F403'
            with open(file=PathVD.conftest_file_path(), mode="w") as file:
                file.write(multiline_string)


    @staticmethod
    def _post_cleanup() -> None:
        PathVD.remove_directory(
            folder_path=PathVD.project_path(), name_contains="__pycache__"
        )
        PathVD.delete_directory(directory_path=PathVD.project_path() / ".pytest_cache")
        if ConfigVD.Pytest.is_delete_conftest():
            PathVD.delete_file(PathVD.conftest_file_path())


    @staticmethod
    def _read_failure_rerun_file() -> str:
        failure_json_path = PathVD.failure_json_file_path()
        failure_json = ""
        if failure_json_path.exists() and ConfigVD.Pytest.is_failure_rerun():
            with open(file=PathVD.failure_json_file_path(), mode="r") as f:
                failure_json = json.load(f)
        return ' '.join(failure_json)
    
    @staticmethod
    def _get_commands(
        allure_result: PathVD,
        allure_report: PathVD,
        pytest_html_report: PathVD,
        pytest_json_report: PathVD,
        pytest_xml_report: PathVD,
    ) -> list[str]:
        dry_run_command: str = (
            f"--collect-only  > {PathVD.pytest_dry_run_file_path()}"
            if ConfigVD.Pytest.is_dry_run()
            else ""
        )
        failure_rerun_command: str = RunnerVD._read_failure_rerun_file() if not ConfigVD.Pytest.is_dry_run() else ""
        parallel_count: int = ConfigVD.Pytest.get_parallel_count()
        tag_name: str = (
            ConfigVD.Pytest.get_tag() if not ConfigVD.Pytest.is_dry_run() and not ConfigVD.Pytest.is_failure_rerun() else ""
        )

        output_command: str = "--capture=tee-sys --tb=no"
        pytest_html_command: str = f"--html={pytest_html_report} --self-contained-html"
        pytest_json_command: str = f"--json={pytest_json_report}"
        pytest_xml_command: str = f"--junitxml={pytest_xml_report}"
        parallel_command: str = f"-n {parallel_count}" if parallel_count > 1 else ""
        parallel_group_command: str = (
            "--dist loadfile"
            if ConfigVD.Pytest.is_parallel_group_by_file()
            else "--dist worksteal"
        )
        tag_command: str = f"-m {tag_name}" if tag_name else ""
        allure_json_command: str = f"--alluredir={allure_result} --allure-no-capture"

        pytest_command: str = f"pytest {dry_run_command} {failure_rerun_command} {tag_command} {output_command} {allure_json_command} {pytest_html_command} {pytest_json_command} {pytest_xml_command} {parallel_command} {parallel_group_command}"
        allure_report_command: str = (
            f"allure generate {allure_result} -o {allure_report} --clean"
        )
        commands: list[str] = []
        commands.append(pytest_command)
        if ConfigVD.Allure.is_allure_generate() and not ConfigVD.Pytest.is_dry_run():
            commands.append(allure_report_command)
            if ConfigVD.Allure.is_allure_open():
                commands.append(f"allure open {allure_report}")
        return commands

    @staticmethod
    def _subprocess_execution(commands: list[str], run_commands: bool = True) -> None:
        if run_commands:
            for command in commands:
                try:
                    subprocess.run(args=command, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error while running pytest: {e}")

    @staticmethod
    def _get_dry_run_count() -> int:
        with open(file=PathVD.pytest_dry_run_file_path(), mode="r") as file:
            content: str = file.read()
        test_case_pattern: re.Pattern[str] = re.compile(pattern=r"<Function\s+\w+\[?\w*]?>")
        matches: list[str] = test_case_pattern.findall(string=content)
        test_case_count: int = len(matches)
        return test_case_count

    @staticmethod
    def _result_report(
        start_time: str, elapsed_time: timedelta, test_result: dict
    ) -> None:
        is_dry_run: bool = ConfigVD.Pytest.is_dry_run()
        summary_data: dict = test_result["summary"]
        total_seconds = int(elapsed_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_time_str: str = f"{hours:02}:{minutes:02}:{seconds:02}"
        ReportVD.print_vd_test_report_summary(
            start_time=start_time,
            elapsed_time=elapsed_time_str,
            passed=summary_data["passed"],
            failed=summary_data["failed"],
            error=summary_data["error"],
            skipped=RunnerVD._get_dry_run_count()
            if is_dry_run
            else summary_data["skipped"],
            total=RunnerVD._get_dry_run_count()
            if is_dry_run
            else summary_data["total"],
        )
        if not is_dry_run:
            ReportVD.write_trend_json(
                start_time=start_time,
                elapsed_time=elapsed_time_str,
                test_result=test_result,
            )
            time.sleep(1)
            ReportVD.write_vd_report_html()
            ReportVD.write_trend_html()

    @staticmethod
    def run() -> None:
        RunnerVD._auto_conftest_file()
        time_now: datetime = datetime.now()
        start_time: str = time_now.strftime(format=ValueVD.test_result_d_t_format())
        if not ConfigVD.Pytest.is_dry_run():
            RunnerVD._pre_cleanup()

        allure_result: PathVD = PathVD.allure_logs_path()
        allure_report: PathVD = PathVD.allure_html_path()
        pytest_html_report: PathVD = PathVD.pytest_html_path() / "pytest.html"
        pytest_json_report: PathVD = PathVD.pytest_json_path() / "pytest.json"
        pytest_xml_report: PathVD = PathVD.pytest_xml_path() / "pytest.xml"

        commands: list[str] = RunnerVD._get_commands(
            allure_result=allure_result,
            allure_report=allure_report,
            pytest_html_report=pytest_html_report,
            pytest_json_report=pytest_json_report,
            pytest_xml_report=pytest_xml_report,
        )

        RunnerVD._subprocess_execution(commands=commands, run_commands=True)
        RunnerVD._post_cleanup()

        end_time: datetime = datetime.now()
        elapsed_time: timedelta = end_time - time_now
        test_result: dict[str, dict | set] = ReportVD.read_pytest_json(
            json_path=pytest_json_report
        )

        RunnerVD._result_report(
            start_time=start_time, elapsed_time=elapsed_time, test_result=test_result
        )
