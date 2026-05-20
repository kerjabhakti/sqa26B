from e2e.pages.app_page import AppPage
from e2e.pages.commute_form_page import CommuteFormPage
from e2e.utils.selectors import by_testid
from e2e.utils.waits import wait_visible


def test_requires_name_and_points(base_url, driver):
    app = AppPage(driver, base_url)
    app.open()
    app.click_add_commute()

    form = CommuteFormPage(driver)
    form.wait_loaded()
    submit = wait_visible(driver, *by_testid("submit-commute"))
    assert submit.get_attribute("disabled")
