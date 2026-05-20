from e2e.pages.app_page import AppPage
from e2e.pages.commute_form_page import CommuteFormPage
from e2e.pages.commute_list_page import CommuteListPage
from e2e.fixtures.commute_data import DEFAULT_COMMUTE, UPDATED_COMMUTE
from e2e.utils.waits import wait_visible
from e2e.utils.selectors import by_testid


def _create_commute(driver, base_url):
    app = AppPage(driver, base_url)
    app.open()
    app.click_add_commute()

    form = CommuteFormPage(driver)
    form.wait_loaded()
    form.set_name(DEFAULT_COMMUTE["name"])
    form.pick_home()
    form.map_click(120, 160)
    form.pick_office()
    form.map_click(220, 220)
    form.select_vehicle(DEFAULT_COMMUTE["vehicle"])
    form.set_fuel_price(DEFAULT_COMMUTE["fuel_price"])
    form.set_days_per_week(DEFAULT_COMMUTE["days_per_week"])
    form.submit()


def test_update_commute(base_url, driver):
    _create_commute(driver, base_url)
    list_page = CommuteListPage(driver)
    list_page.wait_list()
    commute_id = list_page.first_commute_id()
    assert commute_id is not None

    list_page.open_edit(commute_id)
    form = CommuteFormPage(driver)
    form.wait_loaded()
    form.set_name(UPDATED_COMMUTE["name"])
    form.select_vehicle(UPDATED_COMMUTE["vehicle"])
    form.set_fuel_price(UPDATED_COMMUTE["fuel_price"])
    form.set_days_per_week(UPDATED_COMMUTE["days_per_week"])
    form.submit()

    list_page.wait_list()
    assert list_page.read_commute_name(commute_id) == UPDATED_COMMUTE["name"]


def test_route_outputs_render(base_url, driver):
    _create_commute(driver, base_url)
    list_page = CommuteListPage(driver)
    list_page.wait_list()
    commute_id = list_page.first_commute_id()
    assert commute_id is not None
    assert "Rp" in list_page.read_annual_cost(commute_id)
    assert "hari" in list_page.read_annual_workdays(commute_id)
    wait_visible(driver, *by_testid("map"))
