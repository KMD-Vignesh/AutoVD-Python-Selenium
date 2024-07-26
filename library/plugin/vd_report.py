import json
from datetime import datetime

from tabulate import tabulate

from library.composer.vd_path import PathVD
from library.model.vd_class import ValueVD
from library.model.vd_config import ConfigVD


class ReportVD:
    @staticmethod
    def read_screen_shot_json_files():
        directory: PathVD = PathVD.failure_screenshot_path()
        data:dict = {}
        
        for filepath in PathVD(directory).rglob('*.json'):
            with filepath.open(mode='r') as file:
                content = json.load(file)
                if len(content) == 1:
                    key = list(content.keys())[0]
                    value = content[key]
                    data[key] = value
                    
        return data

    @staticmethod
    def read_pytest_json(
        json_path: PathVD = PathVD.pytest_json_path() / "pytest.json",
    ) -> dict[str, dict]:
        summary_data: dict = {}
        failure_data: list[str] = []
        summary_data["testcases"] = []
        if ".json" in str(object=json_path):
            with open(file=json_path, mode="r") as f:
                pytest_json = json.load(f)

            if "report" in pytest_json:
                if "summary" in pytest_json["report"]:
                    for outcome in ["passed", "failed", "skipped", "error"]:
                        summary_data[outcome] = 0
                summary_data["total"] = pytest_json["report"]["summary"]["num_tests"]
                if "tests" in pytest_json["report"]:
                    for tc_li in pytest_json["report"]["tests"]:
                        tc_full_name: str = tc_li["name"]
                        method_name: str = tc_full_name.split(sep="::")[1]
                        file_path: str = tc_full_name.split(sep="::")[0]
                        tc_outcome: str = tc_li["outcome"]
                        summary_data[tc_outcome] = summary_data[tc_outcome] + 1
                        if "failed" in tc_outcome:
                            failure_data.append(tc_full_name)
                        logs: list = []
                        reason: list = []
                        for state in ["setup", "call", "teardown"]:
                            if state in tc_li:
                                if "stderr" in tc_li[state]:
                                    logs.extend(
                                        str(object=tc_li[state]["stderr"]).split(
                                            sep="\n"
                                        )
                                    )
                                if "longrepr" in tc_li[state]:
                                    reason.extend(
                                        str(object=tc_li[state]["longrepr"]).split(
                                            sep="\n"
                                        )
                                    )
                        logs = [item for item in logs if item]
                        reason = [item for item in reason if item]
                        summary_data["testcases"].append(
                            {
                                "name": method_name,
                                "file_path": file_path,
                                "outcome": tc_outcome,
                                "logs": logs,
                                "reason": reason,
                            }
                        )

        return {"summary": summary_data, "failure": failure_data}

    @staticmethod
    def write_trend_json(
        start_time: str, elapsed_time: str, test_result: dict[str, dict | list]
    ) -> None:
        summary_data: dict = test_result["summary"]
        failure_data: list = test_result["failure"]
        trend_json_path: PathVD = PathVD.trend_json_file_path()
        vd_json_path: PathVD = PathVD.vd_json_file_path()
        trend_json: dict = {}
        if trend_json_path.exists() and trend_json_path.stat().st_size > 0:
            try:
                with open(file=trend_json_path, mode="r") as f:
                    trend_json = json.load(fp=f)
            except json.JSONDecodeError:
                print(
                    f"Warning: {trend_json_path} is not a valid JSON file. It will be overwritten."
                )
        with open(file=PathVD.failure_json_file_path(), mode="w") as f:
            json.dump(obj=failure_data, fp=f, indent=4)

        date_split: str = start_time.split(sep=" ")[0]
        time_split: str = start_time.split(sep=" ")[1]
        summary_data["duration"] = elapsed_time
        if date_split in trend_json:
            trend_json[date_split][time_split] = summary_data
        else:
            trend_json[date_split] = {time_split: summary_data}

        vd_json: dict = {}
        vd_json[date_split] = {time_split: summary_data}
        with open(file=trend_json_path, mode="w") as f:
            json.dump(obj=trend_json, fp=f, indent=4)
        with open(file=vd_json_path, mode="w") as f:
            json.dump(obj=vd_json, fp=f, indent=4)

    @staticmethod
    def _common_html_contents(is_trend: bool):
        with open(file=PathVD.vd_css_file_path(), mode="r") as css_file:
            css_content: str = css_file.read()

        with open(file=PathVD.vd_js_file_path(), mode="r") as js_file:
            js_content: str = js_file.read()

        html_title: str = ""

        if is_trend:
            html_title = "Test VD Trend"
            html_path: PathVD = PathVD.trend_html_file_path()
            with open(file=PathVD.trend_json_file_path(), mode="r") as json_file:
                json_content: str = json_file.read()
            mid_html: str = f"""
                                <div id="main">
                                    <div>
                                        <h1>{html_title} - {ConfigVD.Project.get_project_name()}</h1>
                                        <div id="piechart"></div>
                                    </div>
                                    <div class="drop_down">
                                        <label for="date-select">Date : </label>
                                        <select id="date-select" onchange="updateTimeOptions()">
                                        <!-- Date options will be populated dynamically -->
                                        </select>
                                        <span class="divider"></span>
                                        <label for="time-select">Time : </label>
                                        <select id="time-select">
                                        <!-- Time options will be populated dynamically -->
                                        </select>
                                    </div>
                                </div>
                            """
        else:
            html_title = "Test VD Report"
            html_path: PathVD = PathVD.vd_html_file_path()
            with open(file=PathVD.vd_json_file_path(), mode="r") as json_file:
                json_content: str = json_file.read()
                json_dict: dict[str, dict] = json.loads(s=json_content)
            date_str: str = list(json_dict.keys())[0]
            date_obj: datetime = datetime.strptime(date_str, "%d/%m/%y")
            date_json: str = date_obj.strftime(format="%d / %b / %Y")
            time_obj: datetime = datetime.strptime(
                list(json_dict[date_str].keys())[0], "%H:%M:%S"
            )
            time_json: str = time_obj.strftime(format="%I:%M:%S / %p")
            mid_html: str = f"""
                                <div id="main">
                                    <div>
                                        <h1>{html_title} - {ConfigVD.Project.get_project_name()}</h1>
                                        <div id="piechart"></div>
                                    </div>
                                    <div class="drop_down">
                                        <label for="date-select">Date : <span class="class_dt">{date_json}</span></label>
                                        <select class="drop_down_disable" id="date-select" onchange="updateTimeOptions()">
                                        <!-- Date options will be populated dynamically -->
                                        </select>
                                        <span class="divider"></span>
                                        <label for="time-select">Time : <span class="class_dt">{time_json}</span></label>
                                        <select class="drop_down_disable" id="time-select">
                                        <!-- Time options will be populated dynamically -->
                                        </select>
                                    </div>
                                </div>
                            """

        pre_html: str = f"""
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>{html_title}</title>
                                <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
                                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-table@1.23.0/dist/bootstrap-table.min.css">
                                <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
                                <script src="https://cdn.jsdelivr.net/npm/bootstrap-table@1.23.0/dist/bootstrap-table.min.js"></script>
                                <style>
                                    {css_content}
                                </style>
                            </head>
                            <body>
                                <div class="container">
                        """

        post_html: str = f"""
                            <div>
                                <label for="search-tc">Search :</label>
                                <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for names..">
                            </div>
                            <table id="data-table" class="display sortable"   data-toggle="table" data-search="true" data-show-columns="true">
                                                <thead>
                                                    <tr>
                                                        <th aria-sort="ascending">
                                                            <button>
                                                                Test Case Name
                                                                <span aria-hidden="true"></span>
                                                            </button>
                                                        </th>
                                                        <th aria-sort="ascending">
                                                            <button>
                                                                Status
                                                                <span aria-hidden="true"></span>
                                                            </button>
                                                        </th>
                                                        <th aria-sort="ascending">
                                                            <button>
                                                                File Path
                                                                <span aria-hidden="true"></span>
                                                            </button>
                                                        </th>
                                                    </tr>
                                                </thead>
                                                <tbody id="table>
                                                    <!-- Table rows will be inserted here dynamically -->
                                                </tbody>
                                            </table>
                                        </div>
                                        <div class="overlay" id="overlay"></div>

                                        <div class="popup" id="popup">
                                            <div class="popup-header"><h2>Test Case Details</h2></div>
                                            <div class="popup-content" id="popup-content">
                                                <!-- Popup content will be inserted here dynamically -->
                                            </div>
                                            <button class="popup-close" onclick="closePopup()">Close</button>
                                        </div>
                                        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                                        <script>
                                            const data = {json_content};
                                            {js_content}
                                            
                                        </script>
                                    </body>
                                </html>
                            """

        with open(file=html_path, mode="w") as html_file:
            html_file.write(f"{pre_html}{mid_html}{post_html}")
        return html_path

    @staticmethod
    def write_trend_html() -> None:
        return ReportVD._common_html_contents(is_trend=True)

    @staticmethod
    def write_vd_report_html() -> None:
        return ReportVD._common_html_contents(is_trend=False)

    @staticmethod
    def print_vd_test_report_summary(
        start_time: str,
        elapsed_time: str,
        passed: int,
        failed: int,
        error: int,
        skipped: int,
        total: int,
    ) -> None:
        summary_header: list[list[str]] = [
            [
                "",
                "",
                "",
                "",
                f"**** {ValueVD.color_cyan(message='VD Test Report Summary')} ****",
                "",
                "",
                "",
                "",
            ]
        ]
        summary_data: list = [
            [
                ValueVD.color_cyan(message="Start Time"),
                start_time,
                ValueVD.color_cyan(message="Elapsed Time"),
                elapsed_time,
            ],
            [
                ValueVD.color_green(message="Passed"),
                ValueVD.color_red(message="Failed / Error"),
                ValueVD.color_yellow(message="Skipped"),
                ValueVD.color_blue(message="Total"),
            ],
            [passed, failed + error, skipped, total],
        ]
        print(tabulate(tabular_data=summary_header, tablefmt="fancy_grid"))
        print(
            tabulate(
                tabular_data=summary_data,
                tablefmt="fancy_grid",
                stralign="center",
                numalign="center",
            )
        )
