from functools import lru_cache

import yaml

from library.composer.vd_path import PathVD


class ConfigVD:
    @lru_cache
    @staticmethod
    def get_config() -> dict[str, dict]:
        with open(file=PathVD.vd_config_file_path(), mode="r") as f:
            config: dict = yaml.safe_load(stream=f)
        return config

    class Project:
        @staticmethod
        def get_project_name() -> str:
            return ConfigVD.get_config()["Project"]["ProjectName"]

    class Browser:
        @staticmethod
        def is_headless() -> bool:
            return ConfigVD.get_config()["Browser"]["IsHeadless"]

        @staticmethod
        def get_default_browser() -> str:
            return ConfigVD.get_config()["Browser"]["DefaultBrowser"]

        @staticmethod
        def is_multi_browser() -> bool:
            return ConfigVD.get_config()["Browser"]["IsMultiBrowser"]
        
        @staticmethod
        def is_delete_downloads() -> bool:
            return ConfigVD.get_config()["Browser"]["DeleteDownloads"]
        
        @staticmethod
        def get_multi_browser_list() -> list[str]:
            return ConfigVD.get_config()["Browser"]["MultiBrowserList"]

    class URL:
        @staticmethod
        def get(key: str) -> str:
            return ConfigVD.get_config()["URL"][key]

        @staticmethod
        def find_name_url_list(value: str) -> str:
            for key, url in ConfigVD.get_config()["URL"].items():
                if value in url:
                    return key
            return ""

    class Credentials:
        @staticmethod
        def get(key: str) -> str:
            return ConfigVD.get_config()["Credentials"][key]

    class Pytest:
        @staticmethod
        def is_dry_run() -> bool:
            return ConfigVD.get_config()["Pytest"]["IsDryRun"]
        
        @staticmethod
        def is_failure_rerun() -> bool:
            return ConfigVD.get_config()["Pytest"]["IsFailureRerun"]

        @staticmethod
        def get_parallel_count() -> int:
            value: int | None = ConfigVD.get_config()["Pytest"]["ParallelCount"]
            if value:
                return int(value)
            else:
                return 1

        @staticmethod
        def is_parallel_group_by_file() -> bool:
            return ConfigVD.get_config()["Pytest"]["IsParallelGroupFile"]

        @staticmethod
        def is_delete_conftest() -> bool:
            return ConfigVD.get_config()["Pytest"]["DeleteConftest"]

        @staticmethod
        def get_tag() -> str:
            return ConfigVD.get_config()["Pytest"]["Tag"]

    class Allure:
        @staticmethod
        def is_allure_generate() -> bool:
            return ConfigVD.get_config()["Allure"]["Generate"]

        @staticmethod
        def is_allure_open() -> bool:
            return ConfigVD.get_config()["Allure"]["AutoOpenServer"]
