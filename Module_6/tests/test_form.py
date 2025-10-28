from datetime import datetime

from playwright.sync_api import Page, expect


def test_form_input(page: Page):
    page.goto("https://demoqa.com/automation-practice-form")
    page.get_by_role("heading", name="Practice Form").is_visible()
    page.get_by_role("textbox", name="First Name").clear()
    page.get_by_role("textbox", name="First Name").fill("Nikita")
    page.get_by_role("textbox", name="Last Name").type("Atikin")
    page.get_by_role("textbox", name="name@example.com").fill("scam@avito.com")
    page.get_by_role("textbox", name="Mobile").fill("1234567890")
    page.get_by_text("Male", exact=True).click()

    value = page.locator("#dateOfBirthInput").get_attribute("value")
    today = datetime.now().strftime("%d %b %Y")
    assert value == today, f"Ожидалось значение по умолчанию = {today}, но получили {value}"

    page.locator("#subjectsInput").type("English")
    page.locator("#react-select-2-option-0").click()
    page.get_by_text("Sports").click()
    page.get_by_text("Music").click()
    page.fill("#currentAddress", "123qwert, Moscow")

    page.locator("#state").click()
    page.get_by_text("NCR", exact=True).click()
    page.locator("#city").click()
    page.get_by_text("Delhi", exact=True).click()

    page.get_by_role("button", name="Submit").click()

    footer_text = page.locator("footer").inner_text()
    expected_footer = "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."
    assert expected_footer in footer_text, f"Footer text mismatch. Expected '{expected_footer}' but got '{footer_text}'"

def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")

    yes = page.get_by_role("radio", name="Yes")
    impressive = page.get_by_role("radio", name="Impressive")
    no = page.get_by_role("radio", name="No")

    expect(no).to_be_disabled()
    expect(yes).to_be_enabled()
    expect(impressive).to_be_enabled()

    page.locator('[for="yesRadio"]').click()
    expect(yes).to_be_checked()
    expect(impressive).not_to_be_checked()

def test_checkbox_visibility(page: Page):
    page.goto("https://demoqa.com/checkbox")
    home = page.get_by_text("Home", exact=True)
    desktop = page.get_by_text("Desktop", exact=True)

    assert home.is_visible(), "Элемент 'Home' должен быть видим"
    assert not desktop.is_visible(), "Элемент 'Desktop' не должен быть видим до раскрытия"

    page.locator(".rct-icon-expand-close").click()
    assert desktop.is_visible(), "После раскрытия 'Desktop' должен быть видим"

def test_visible_after_5_seconds(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")

    visible_after_button = page.get_by_text("Visible After 5 Seconds")
    assert not visible_after_button.is_visible(), "Элемент не должен быть видим сразу после загрузки"

    page.wait_for_selector("#visibleAfter", state="visible", timeout=10000)
    assert visible_after_button.is_visible(), "Элемент должен стать видимым после 5 секунд"