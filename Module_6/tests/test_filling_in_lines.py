from playwright.sync_api import Page

def test_input(page: Page):
    page.goto("https://demoqa.com/webtables")
    page.get_by_role("button", name="Add").click()
    page.get_by_text("Registration Form").is_visible()
    page.get_by_placeholder("First Name").fill("Nikita")
    page.get_by_placeholder("Last Name").fill("Atikin")
    page.get_by_placeholder("name@example.com").fill("phototita@no.com")
    page.get_by_placeholder("Age").fill("24")
    page.get_by_placeholder("Salary").fill("24")
    page.get_by_placeholder("Department").fill("GOVNA")
    page.get_by_role("button", name="Submit")

