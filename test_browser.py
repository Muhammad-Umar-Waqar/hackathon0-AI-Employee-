"""Simple browser test"""
from playwright.sync_api import sync_playwright

print("Opening browser...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    print("Opening LinkedIn...")
    page.goto('https://www.linkedin.com/login')
    print("Browser is open! Log in to LinkedIn.")
    print("Keep browser open for 30 seconds...")
    import time
    time.sleep(30)
    browser.close()
print("Done!")
