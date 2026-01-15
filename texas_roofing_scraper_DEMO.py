"""
Texas Roofing Company Lead Generator - DEMO VERSION
===================================================

This is a DEMO version with only 3 zip codes per city for quick testing.
Perfect for testing if everything is set up correctly before running the full scan.

Expected runtime: 10-15 minutes

For the full version with all zip codes, use: texas_roofing_scraper.py
"""

import re
import time
import random
from playwright.sync_api import sync_playwright
from tqdm import tqdm
import pandas as pd

# ============================================================================
# DEMO TEXAS MARKETS (ONLY 3 ZIP CODES PER CITY FOR TESTING)
# ============================================================================

TEXAS_MARKETS = {
    "Houston": ["77002", "77019", "77056"],  # Only 3 zips for demo
    "Dallas": ["75201", "75206", "75219"],   # Only 3 zips for demo
    "Austin": ["78701", "78704", "78731"],   # Only 3 zips for demo
}

# ============================================================================
# KEYWORD LIST FOR TIER 1 CLASSIFICATION
# ============================================================================

TARGET_KEYWORDS = [
    "fluid applied",
    "silicone coating",
    "acrylic coating",
    "roof restoration",
    "aluminum coating",
    "elastomeric",
    "polyurethane",
    "commercial roof coating",
    "liquid applied",
    "cool roof",
    "white roof",
    "waterproofing",
    "PMMA"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_emails(text):
    """Extract email addresses from text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return list(set(emails))


def check_for_keywords(text):
    """Check if any target keywords appear in the text."""
    text_lower = text.lower()
    found_keywords = []
    for keyword in TARGET_KEYWORDS:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
    return found_keywords


def clean_phone_number(phone):
    """Clean and standardize phone numbers."""
    if not phone:
        return ""
    cleaned = re.sub(r'[^\d]', '', phone)
    return cleaned


def is_duplicate(company_name, phone, existing_leads):
    """Check if a lead already exists."""
    phone_cleaned = clean_phone_number(phone)
    for lead in existing_leads:
        existing_phone = clean_phone_number(lead.get('Phone', ''))
        existing_name = lead.get('Company Name', '').strip().lower()
        current_name = company_name.strip().lower()
        if phone_cleaned and existing_phone and phone_cleaned == existing_phone:
            return True
        if current_name and existing_name and current_name == existing_name:
            return True
    return False


def is_valid_url(url):
    """Check if a URL is valid and can be navigated to."""
    if not url or url.strip() == "":
        return False
    url = url.strip()
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
    try:
        if any(char in url for char in ['<', '>', '{', '}', '|', '\\', '^', '`', '"']):
            return False
        if '.' not in url:
            return False
        if url in ['http://', 'https://']:
            return False
        return True
    except:
        return False


def clean_url(url):
    """Clean and normalize a URL before attempting to visit it."""
    if not url or url.strip() == "":
        return None
    url = url.strip().strip('\'"')
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    url = url.replace(' ', '')
    if is_valid_url(url):
        return url
    else:
        return None


def find_search_box(page):
    """Try multiple selectors to find the Google Maps search box."""
    selectors = [
        'input[id="searchboxinput"]',
        'input[name="q"]',
        'input[aria-label*="Search"]',
        '#searchboxinput',
        'form input[type="text"]',
        '[role="search"] input'
    ]

    for selector in selectors:
        try:
            element = page.locator(selector).first
            if element.count() > 0 and element.is_visible(timeout=2000):
                return element
        except:
            continue

    return None


def scrape_google_maps_results(page, city, zip_code):
    """Scrape roofing companies from Google Maps."""
    search_query = f"Roofing company in {city} {zip_code}"
    companies = []

    try:
        page.goto("https://www.google.com/maps", timeout=30000)
        time.sleep(3)

        # Handle cookie consent dialog if it appears
        try:
            # Try to click "Accept all" or "Reject all" button for cookies
            accept_button = page.locator('button:has-text("Accept all"), button:has-text("Reject all"), form:has-text("Accept") >> button').first
            if accept_button.is_visible(timeout=3000):
                accept_button.click()
                time.sleep(2)
        except:
            pass  # No cookie dialog or already accepted

        # Try multiple selectors to find search box
        search_box = find_search_box(page)

        if not search_box:
            raise Exception("Could not find search box with any known selector")

        # Scroll to search box and interact
        search_box.scroll_into_view_if_needed()
        time.sleep(0.5)
        search_box.click()
        time.sleep(0.5)
        search_box.fill(search_query)
        time.sleep(0.5)
        search_box.press("Enter")
        time.sleep(5)  # Increased wait time for results to load

        results_panel = page.locator('div[role="feed"]').first
        for _ in range(3):
            try:
                results_panel.evaluate("element => element.scrollBy(0, 1000)")
                time.sleep(1)
            except:
                pass

        result_items = page.locator('div[role="article"]').all()

        for item in result_items[:20]:
            try:
                name_elem = item.locator('div.fontHeadlineSmall').first
                company_name = name_elem.inner_text() if name_elem.count() > 0 else ""

                if not company_name:
                    continue

                item.click()
                time.sleep(1.5)

                phone = ""
                try:
                    phone_button = page.locator('button[data-item-id*="phone"]').first
                    if phone_button.count() > 0:
                        phone_text = phone_button.get_attribute('data-item-id')
                        if phone_text:
                            phone = phone_text.split(':')[-1] if ':' in phone_text else ""
                except:
                    pass

                website = ""
                try:
                    website_link = page.locator('a[data-item-id="authority"]').first
                    if website_link.count() > 0:
                        website = website_link.get_attribute('href')
                except:
                    pass

                address = ""
                try:
                    address_button = page.locator('button[data-item-id="address"]').first
                    if address_button.count() > 0:
                        address = address_button.inner_text()
                except:
                    pass

                companies.append({
                    'Company Name': company_name,
                    'Phone': phone,
                    'Website': website,
                    'Address': address,
                    'City': city,
                    'Zip Code Used': zip_code
                })

            except Exception as e:
                continue

    except Exception as e:
        print(f"  ⚠️  Error scraping {city} {zip_code}: {str(e)}")

    return companies


def classify_lead_tier(company, page, verbose=False):
    """Classify a lead into Tier 1, 2, or 3 with optional verbose logging."""
    company_name = company.get('Company Name', 'Unknown')
    website = company.get('Website', '')

    if not website or website.strip() == "":
        if verbose:
            print(f"         ℹ️  No website → Tier 2")
        return "Tier 2", [], []

    # Clean and validate URL before attempting to visit
    cleaned_url = clean_url(website)

    if not cleaned_url:
        if verbose:
            print(f"         ⚠️  Invalid URL format → Tier 3")
        return "Tier 3", [], []

    try:
        if verbose:
            print(f"         🌐 Checking {cleaned_url[:50]}...")

        # Reduced delay but still anti-bot
        time.sleep(random.uniform(2, 4))

        # Increased timeout for slow websites (using cleaned URL)
        page.goto(cleaned_url, timeout=20000, wait_until='domcontentloaded')
        time.sleep(2)

        page_text = page.inner_text('body')
        emails = extract_emails(page_text)
        keywords_found = check_for_keywords(page_text)

        if keywords_found:
            if verbose:
                print(f"         ✅ TIER 1! Found: {', '.join(keywords_found[:3])}")
            return "Tier 1", keywords_found, emails
        else:
            if verbose:
                print(f"         📄 Tier 3 (no keywords found)")
            return "Tier 3", [], emails

    except Exception as e:
        error_msg = str(e)[:80]
        if verbose:
            print(f"         ⚠️  Tier 3 (error: {error_msg})")
        return "Tier 3", [], []


# ============================================================================
# MAIN SCRAPER FUNCTION
# ============================================================================

def scrape_texas_roofing_companies():
    """Main scraping function."""
    print("=" * 80)
    print("🏢 TEXAS ROOFING COMPANY LEAD GENERATOR - DEMO VERSION (VERBOSE)")
    print("=" * 80)
    print("⚡ This demo version scans only 3 zip codes per city for quick testing")
    print("🔍 VERBOSE MODE: You'll see detailed tier classification for each lead")
    print(f"📍 Cities to scan: {', '.join(TEXAS_MARKETS.keys())}")
    print(f"📊 Total zip codes: {sum(len(zips) for zips in TEXAS_MARKETS.values())}")
    print("⏱️  Expected runtime: 15-20 minutes")
    print("=" * 80)
    print()

    all_leads = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        for city, zip_codes in TEXAS_MARKETS.items():
            print(f"\n🌆 Starting {city.upper()}")
            print(f"   Scanning {len(zip_codes)} zip codes...\n")

            for zip_code in tqdm(zip_codes, desc=f"   {city}", unit="zip"):
                print(f"\n      📍 Zip: {zip_code}")
                companies = scrape_google_maps_results(page, city, zip_code)
                print(f"         Found {len(companies)} companies, classifying...")

                for company in companies:
                    if is_duplicate(company['Company Name'], company['Phone'], all_leads):
                        print(f"         ⏭️  {company['Company Name'][:40]}: Duplicate")
                        continue

                    print(f"      📋 {company['Company Name'][:45]}")
                    tier, keywords, emails = classify_lead_tier(company, page, verbose=True)

                    company['Lead Tier'] = tier
                    company['Keywords Found'] = ', '.join(keywords) if keywords else ''
                    company['Email'] = ', '.join(emails) if emails else ''

                    all_leads.append(company)

                time.sleep(1)

            print(f"   ✅ {city} complete! Found {len([l for l in all_leads if l['City'] == city])} unique leads.")

        browser.close()

    print(f"\n{'=' * 80}")
    print(f"💾 Exporting results to Excel...")

    if all_leads:
        df = pd.DataFrame(all_leads)

        column_order = [
            'City', 'Lead Tier', 'Company Name', 'Phone', 'Email',
            'Website', 'Keywords Found', 'Address', 'Zip Code Used'
        ]
        df = df[column_order]
        df = df.sort_values(['City', 'Lead Tier'])

        output_file = 'texas_roofing_leads_DEMO.xlsx'
        df.to_excel(output_file, index=False, engine='openpyxl')

        print(f"✅ SUCCESS! Saved {len(all_leads)} unique leads to '{output_file}'")
        print(f"\n📊 LEAD BREAKDOWN:")
        print(f"   Tier 1 (High Value): {len([l for l in all_leads if l['Lead Tier'] == 'Tier 1'])}")
        print(f"   Tier 2 (Opportunity): {len([l for l in all_leads if l['Lead Tier'] == 'Tier 2'])}")
        print(f"   Tier 3 (Low Value): {len([l for l in all_leads if l['Lead Tier'] == 'Tier 3'])}")
    else:
        print("⚠️  No leads found. Please check your internet connection and try again.")

    print("=" * 80)
    print("🎉 DEMO scraping complete!")
    print("💡 To run the full version with all zip codes, use: texas_roofing_scraper.py")
    print("=" * 80)


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        scrape_texas_roofing_companies()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        print("Please check the error message and try again.")
