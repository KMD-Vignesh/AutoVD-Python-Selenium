import pytest
from pages.sauce_lab.main_page import MainPage

from library.helper.vd_selenium import SeleniumVD
from library.model.vd_config import ConfigVD


@pytest.mark.vignesh
@pytest.mark.remove_cart
def test_add_cart_badge_validation_fail(selenium: SeleniumVD) -> None:
    main_page = MainPage(selenium=selenium)
    main_page.open_app(url=ConfigVD.URL.get(key="SauceLab")).login_to_app(
        username=ConfigVD.Credentials.get(key="UserName"),
        password=ConfigVD.Credentials.get(key="Password"),
    ).assert_true(condition=main_page.is_main_page_loaded()).log(selenium.get_random_text_with_number(10))
