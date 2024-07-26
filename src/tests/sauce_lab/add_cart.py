import pytest
from pages.sauce_lab.main_page import MainPage

from library.helper.vd_selenium import SeleniumVD
from library.model.vd_config import ConfigVD


@pytest.mark.vignesh
@pytest.mark.add_cart
def test_add_cart_badge_validation(selenium: SeleniumVD) -> None:
    main_page = MainPage(selenium=selenium)
    main_page.open_app(url=ConfigVD.URL.get(key="SauceLab")).login_to_app(
        username=ConfigVD.Credentials.get(key="UserName"),
        password=ConfigVD.Credentials.get(key="Password"),
    ).assert_true(condition=main_page.is_main_page_loaded()).add_cart_product(
        product_name="Sauce Labs Bike Light"
    ).assert_true(condition=main_page.get_product_count_badge() == 1).add_cart_product(
        product_name="Sauce Labs Backpack"
    ).assert_true(condition=main_page.get_product_count_badge() == 2).add_cart_product(
        product_name="Sauce Labs Onesie"
    ).assert_true(condition=main_page.get_product_count_badge() == 3)


@pytest.mark.vignesh
@pytest.mark.add_cart
def test_add_cart_badge_validation_fail(selenium: SeleniumVD) -> None:
    main_page = MainPage(selenium=selenium)
    main_page.open_app(url=ConfigVD.URL.get(key="SauceLab")).login_to_app(
        username=ConfigVD.Credentials.get(key="UserName"),
        password=ConfigVD.Credentials.get(key="Password"),
    ).assert_true(condition=main_page.is_main_page_loaded()).add_cart_product(
        product_name="Sauce Labs Bike Light"
    ).assert_true(
        condition=main_page.get_product_count_badge() == 5,
        failure_message=f"{main_page.get_product_count_badge()} == 5",
    )


@pytest.mark.vignesh
@pytest.mark.add_cart
@pytest.mark.skip("Failure Testcase")
def test_add_cart_multi_instances(selenium: SeleniumVD) -> None:
    main_page = MainPage(selenium=selenium)
    main_page.open_app(url=ConfigVD.URL.get(key="SauceLab")).login_to_app(
        username=ConfigVD.Credentials.get(key="UserName"),
        password=ConfigVD.Credentials.get(key="Password"),
    ).assert_true(condition=main_page.is_main_page_loaded()).add_cart_product(
        product_name="Sauce Labs Onesie"
    ).assert_true(condition=main_page.get_product_count_badge() == 1)

    selenium.new_driver_instance(instance_name="firefox", browser_name="firefox")
    main_page.open_app(url=ConfigVD.URL.get(key="SauceLab")).login_to_app(
        username=ConfigVD.Credentials.get(key="UserName"),
        password=ConfigVD.Credentials.get(key="Password"),
    ).assert_true(condition=main_page.is_main_page_loaded()).add_cart_product(
        product_name="Sauce Labs Fleece Jacket"
    ).assert_true(condition=main_page.get_product_count_badge() == 1)

    selenium.switch_driver_instance()
    main_page.add_cart_product(product_name="Sauce Labs Fleece Jacket").assert_true(
        condition=main_page.get_product_count_badge() == 2
    )

    selenium.switch_driver_instance(instance_name="firefox")
    main_page.add_cart_product(product_name="Sauce Labs Onesie").assert_true(
        condition=main_page.get_product_count_badge() == 2
    )
