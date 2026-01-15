"""
Google Maps Connection Test - Diagnostic Tool
==============================================

This script tests if you can connect to Google Maps successfully.
It will take a screenshot to show you what Google is displaying.

Run this if you're getting timeout errors!
"""

from playwright.sync_api import sync_playwright
import time

print("=" * 80)
print("🔍 GOOGLE MAPS CONNECTION TEST")
print("=" * 80)
print()
print("This will:")
print("  1. Open Google Maps")
print("  2. Take a screenshot to show what's on the page")
print("  3. Try to find the search box")
print("  4. Tell you what's blocking the scraper")
print()
print("=" * 80)
print()

with sync_playwright() as p:
    print("🌐 Launching browser...")
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    page = context.new_page()

    print("📍 Navigating to Google Maps...")
    page.goto("https://www.google.com/maps", timeout=30000)
    time.sleep(3)

    print("📸 Taking screenshot 1 (initial page load)...")
    page.screenshot(path="google_maps_test_1_initial.png")
    print("   ✅ Saved: google_maps_test_1_initial.png")
    print()

    # Check for cookie consent
    print("🍪 Checking for cookie consent dialog...")
    try:
        cookie_buttons = page.locator('button:has-text("Accept"), button:has-text("Reject"), button:has-text("I agree")').all()
        if len(cookie_buttons) > 0:
            print(f"   ⚠️  Found {len(cookie_buttons)} cookie consent button(s)!")
            print("   Buttons found:")
            for i, btn in enumerate(cookie_buttons[:5]):
                try:
                    text = btn.inner_text(timeout=1000)
                    print(f"     - {text}")
                except:
                    pass

            print()
            print("   Clicking the first cookie button...")
            cookie_buttons[0].click()
            time.sleep(2)

            print("📸 Taking screenshot 2 (after cookie consent)...")
            page.screenshot(path="google_maps_test_2_after_cookies.png")
            print("   ✅ Saved: google_maps_test_2_after_cookies.png")
        else:
            print("   ✅ No cookie consent dialog found")
    except Exception as e:
        print(f"   ℹ️  No cookie dialog detected: {str(e)[:100]}")

    print()

    # Check for CAPTCHA
    print("🤖 Checking for CAPTCHA...")
    try:
        captcha = page.locator('iframe[src*="recaptcha"], div:has-text("I\'m not a robot")').first
        if captcha.is_visible(timeout=2000):
            print("   ⚠️  CAPTCHA DETECTED! Google is blocking automation.")
            print("   This is why the scraper isn't working.")
            print()
            print("   Solutions:")
            print("     1. Wait a few hours and try again")
            print("     2. Use a different internet connection")
            print("     3. Consider using a proxy/VPN")
        else:
            print("   ✅ No CAPTCHA detected")
    except:
        print("   ✅ No CAPTCHA detected")

    print()

    # Check for search box
    print("🔍 Looking for search box...")
    try:
        search_box = page.locator('input[id="searchboxinput"]')
        if search_box.is_visible(timeout=5000):
            print("   ✅ Search box found and visible!")
            print()
            print("   Testing search functionality...")
            search_box.click()
            time.sleep(0.5)
            search_box.fill("Test roofing company")
            time.sleep(0.5)

            print("📸 Taking screenshot 3 (search box filled)...")
            page.screenshot(path="google_maps_test_3_search_filled.png")
            print("   ✅ Saved: google_maps_test_3_search_filled.png")

            search_box.press("Enter")
            time.sleep(5)

            print("📸 Taking screenshot 4 (search results)...")
            page.screenshot(path="google_maps_test_4_results.png")
            print("   ✅ Saved: google_maps_test_4_results.png")

            print()
            print("   ✅ Search is working!")

        else:
            print("   ❌ Search box NOT visible!")
    except Exception as e:
        print(f"   ❌ Error finding search box: {str(e)[:200]}")
        print()
        print("📸 Taking screenshot 5 (error state)...")
        page.screenshot(path="google_maps_test_5_error.png")
        print("   ✅ Saved: google_maps_test_5_error.png")

    print()
    print("=" * 80)
    print("🔍 PAGE ANALYSIS")
    print("=" * 80)

    # Get page title
    try:
        title = page.title()
        print(f"Page Title: {title}")
    except:
        print("Page Title: Unable to get title")

    # Get current URL
    try:
        url = page.url
        print(f"Current URL: {url}")
    except:
        print("Current URL: Unable to get URL")

    print()
    print("🎯 Keeping browser open for 10 seconds so you can see the page...")
    print("   Look at the browser window to see what Google is showing.")
    time.sleep(10)

    browser.close()

print()
print("=" * 80)
print("✅ TEST COMPLETE!")
print("=" * 80)
print()
print("📊 RESULTS:")
print()
print("Screenshots saved in the current folder:")
print("  - google_maps_test_1_initial.png")
print("  - google_maps_test_2_after_cookies.png (if cookies found)")
print("  - google_maps_test_3_search_filled.png (if search box found)")
print("  - google_maps_test_4_results.png (if search worked)")
print("  - google_maps_test_5_error.png (if error occurred)")
print()
print("Look at the screenshots to see what's blocking the scraper!")
print()
print("Common issues:")
print("  1. Cookie consent dialog blocking the search box")
print("  2. CAPTCHA verification required")
print("  3. Google detected automation and is blocking")
print("  4. Your IP has been rate-limited")
print()
print("=" * 80)
