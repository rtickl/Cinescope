from playwright.sync_api import Page, expect
from random import randint
import time


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[data-qa-id="register_full_name_input"]'
    email_loacor = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    user_email = f'test_{randint(1, 9999)}@email.qa'

    page.fill(username_locator, 'Жмышенко Валерий Альбертович')
    page.fill(email_loacor, user_email)
    page.fill(password_locator, 'qwerty123Q')
    page.fill(repeat_password_locator, 'qwerty123Q')

    page.click('[data-qa-id="register_submit_button"]')

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

    time.sleep(10)
