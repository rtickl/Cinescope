from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("http://demoqa.com/")
    page.locator("svg").first.click()
    page.get_by_text("Text Box").click()
    page.get_by_role("textbox", name="Full Name").click()
    page.get_by_role("textbox", name="Full Name").fill("Name_example")
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill("main@example.com")
    page.get_by_role("textbox", name="Current Address").click()
    page.get_by_role("textbox", name="Current Address").fill("Address")
    page.get_by_role("textbox", name="Current Address").click()
    page.locator("#permanentAddress").click()
    page.locator("#permanentAddress").fill("address")
    page.get_by_role("button", name="Submit").click()
    expect(page.locator("#name")).to_contain_text("Name:Name_example")
    page.get_by_text("Email:main@example.com").click()
    expect(page.locator("#email")).to_contain_text("Email:main@example.com")
    # expect(page.locator("#output")).to_contain_text("Current Address:Address")
    # expect(page.locator("#output")).to_contain_text("Permananet Address:address")
