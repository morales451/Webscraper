"""
Enhanced Google Maps Diagnostic - Find The Search Box
======================================================

This will try MULTIPLE ways to find the search box and show you what's on the page.
"""

from playwright.sync_api import sync_playwright
import time

print("=" * 80)
print("🔍 ENHANCED GOOGLE MAPS DIAGNOSTIC")
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
    time.sleep(5)  # Wait longer for page to fully load

    print("📸 Taking screenshot of initial page...")
    page.screenshot(path="diagnostic_1_initial.png", full_page=True)
    print("   ✅ Saved: diagnostic_1_initial.png")
    print()

    # Get page info
    print("=" * 80)
    print("📊 PAGE INFORMATION")
    print("=" * 80)
    print(f"Title: {page.title()}")
    print(f"URL: {page.url}")
    print()

    # Try multiple selectors for the search box
    print("=" * 80)
    print("🔍 TRYING MULTIPLE SELECTORS FOR SEARCH BOX")
    print("=" * 80)
    print()

    selectors = [
        'input[id="searchboxinput"]',
        'input[name="q"]',
        'input[aria-label*="Search"]',
        'input[placeholder*="Search"]',
        '#searchboxinput',
        'form input[type="text"]',
        'input.searchboxinput',
        '[role="search"] input',
        'input[autocomplete="off"]'
    ]

    found_selector = None

    for i, selector in enumerate(selectors, 1):
        print(f"[{i}/{len(selectors)}] Trying: {selector}")
        try:
            element = page.locator(selector).first
            count = element.count()

            if count > 0:
                is_visible = element.is_visible(timeout=2000)
                print(f"   ✅ FOUND! Count: {count}, Visible: {is_visible}")

                if is_visible and not found_selector:
                    found_selector = selector
                    print(f"   🎯 This one looks good! We'll use this.")

                    # Try to get more info about this element
                    try:
                        placeholder = element.get_attribute('placeholder')
                        print(f"   Placeholder text: {placeholder}")
                    except:
                        pass

                    try:
                        aria_label = element.get_attribute('aria-label')
                        print(f"   Aria-label: {aria_label}")
                    except:
                        pass

            else:
                print(f"   ❌ Not found")

        except Exception as e:
            print(f"   ❌ Error: {str(e)[:80]}")

        print()

    print("=" * 80)
    print()

    if found_selector:
        print(f"✅ SUCCESS! Found working selector: {found_selector}")
        print()
        print("🧪 Testing search functionality...")
        print()

        try:
            search_box = page.locator(found_selector).first

            # Scroll to element
            search_box.scroll_into_view_if_needed()
            time.sleep(0.5)

            # Click and fill
            search_box.click()
            time.sleep(0.5)

            test_query = "Roofing company in Houston 77002"
            print(f"Typing: {test_query}")
            search_box.fill(test_query)
            time.sleep(1)

            print("📸 Taking screenshot after typing...")
            page.screenshot(path="diagnostic_2_typed.png", full_page=True)
            print("   ✅ Saved: diagnostic_2_typed.png")
            print()

            print("Pressing Enter...")
            search_box.press("Enter")
            time.sleep(7)  # Wait for results

            print("📸 Taking screenshot of results...")
            page.screenshot(path="diagnostic_3_results.png", full_page=True)
            print("   ✅ Saved: diagnostic_3_results.png")
            print()

            # Check if we got results
            try:
                results = page.locator('div[role="article"]').all()
                print(f"✅ Found {len(results)} results on the page!")
                print()

                if len(results) > 0:
                    print("🎉 SEARCH IS WORKING!")
                    print()
                    print("=" * 80)
                    print("🎯 USE THIS SELECTOR IN THE SCRAPER:")
                    print("=" * 80)
                    print(f"   {found_selector}")
                    print("=" * 80)
                else:
                    print("⚠️  Search executed but no results found")

            except Exception as e:
                print(f"⚠️  Couldn't verify results: {str(e)[:100]}")

        except Exception as e:
            print(f"❌ Error during search test: {str(e)}")
            page.screenshot(path="diagnostic_error.png", full_page=True)
            print("   Saved error screenshot: diagnostic_error.png")

    else:
        print("❌ COULD NOT FIND SEARCH BOX with any selector!")
        print()
        print("Let's check what input fields ARE on the page...")
        print()

        try:
            all_inputs = page.locator('input').all()
            print(f"Found {len(all_inputs)} total input fields on the page:")
            print()

            for i, inp in enumerate(all_inputs[:10], 1):  # Show first 10
                try:
                    inp_type = inp.get_attribute('type') or 'text'
                    inp_id = inp.get_attribute('id') or '(no id)'
                    inp_name = inp.get_attribute('name') or '(no name)'
                    inp_placeholder = inp.get_attribute('placeholder') or '(no placeholder)'
                    is_visible = inp.is_visible(timeout=1000)

                    print(f"{i}. Type: {inp_type}, ID: {inp_id}, Name: {inp_name}")
                    print(f"   Placeholder: {inp_placeholder}, Visible: {is_visible}")
                    print()

                except:
                    print(f"{i}. (couldn't get info)")
                    print()

        except Exception as e:
            print(f"Error listing inputs: {str(e)}")

    print()
    print("🎯 Keeping browser open for 15 seconds - look at the page!")
    print("   What do you see? Is there a search box visible?")
    print()
    time.sleep(15)

    browser.close()

print()
print("=" * 80)
print("✅ DIAGNOSTIC COMPLETE!")
print("=" * 80)
print()
print("📸 Screenshots saved:")
print("   - diagnostic_1_initial.png")
print("   - diagnostic_2_typed.png (if search box found)")
print("   - diagnostic_3_results.png (if search worked)")
print()

if found_selector:
    print("🎉 GOOD NEWS! Found a working selector:")
    print(f"   {found_selector}")
    print()
    print("I'll update the scraper to use this selector!")
else:
    print("⚠️  Could not find search box automatically.")
    print()
    print("Please look at diagnostic_1_initial.png and tell me:")
    print("  1. Do you see a search box on the page?")
    print("  2. What does it say (placeholder text)?")
    print("  3. Is the page in English or another language?")
    print("  4. Does the page look normal or is there an error?")

print()
print("=" * 80)
