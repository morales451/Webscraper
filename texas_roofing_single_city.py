"""
Texas Roofing Company Lead Generator - SINGLE CITY VERSION
==========================================================

Choose ONE city to focus on and scan all its zip codes.
Perfect for focused prospecting in a specific market!

This version also has VERBOSE logging so you can see:
- Which websites are being visited
- Whether keywords are found
- Why leads are classified as Tier 1, 2, or 3
"""

import re
import time
import random
from playwright.sync_api import sync_playwright
from tqdm import tqdm
import pandas as pd

# ============================================================================
# TEXAS MARKETS DICTIONARY
# ============================================================================

TEXAS_MARKETS = {
    "Houston": [
        "77002", "77003", "77004", "77005", "77006", "77007", "77008", "77009",
        "77010", "77019", "77020", "77021", "77025", "77027", "77030", "77035",
        "77036", "77042", "77045", "77047", "77051", "77054", "77056", "77057",
        "77063", "77064", "77072", "77077", "77081", "77084"
    ],
    "Dallas": [
        "75201", "75202", "75203", "75204", "75205", "75206", "75207", "75208",
        "75209", "75210", "75211", "75212", "75214", "75215", "75216", "75217",
        "75218", "75219", "75220", "75223", "75224", "75225", "75226", "75227",
        "75228", "75229", "75230", "75231", "75232", "75233"
    ],
    "Austin": [
        "78701", "78702", "78703", "78704", "78705", "78717", "78721", "78722",
        "78723", "78724", "78725", "78726", "78727", "78728", "78729", "78730",
        "78731", "78732", "78733", "78734", "78735", "78736", "78737", "78738",
        "78739", "78741", "78742", "78744", "78745", "78746"
    ],
    "San Antonio": [
        "78201", "78202", "78203", "78204", "78205", "78207", "78208", "78209",
        "78210", "78211", "78212", "78213", "78214", "78215", "78216", "78217",
        "78218", "78219", "78220", "78221", "78222", "78223", "78224", "78225",
        "78226", "78227", "78228", "78229", "78230", "78231"
    ],
    "Fort Worth": [
        "76101", "76102", "76103", "76104", "76105", "76106", "76107", "76108",
        "76109", "76110", "76111", "76112", "76114", "76115", "76116", "76117",
        "76118", "76119", "76120", "76122", "76123", "76126", "76127", "76129",
        "76131", "76132", "76133", "76134", "76135", "76137"
    ]
}

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

    # Handle Google Maps redirect URLs (both absolute and relative)
    # Google sometimes wraps URLs like: https://www.google.com/url?q=https://actualwebsite.com
    # Or as relative URLs like: /url?q=https://actualwebsite.com&opi=...
    if 'google.com/url?q=' in url or url.startswith('/url?q='):
        try:
            # Extract the actual URL from Google's redirect
            actual_url = url.split('?q=')[1].split('&')[0]
            # URL decode if needed
            from urllib.parse import unquote
            url = unquote(actual_url)
        except:
            pass

    # Handle URLs that start with www. but no protocol
    if url.startswith('www.'):
        url = 'https://' + url

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

        try:
            accept_button = page.locator('button:has-text("Accept all"), button:has-text("Reject all"), form:has-text("Accept") >> button').first
            if accept_button.is_visible(timeout=3000):
                accept_button.click()
                time.sleep(2)
        except:
            pass

        search_box = find_search_box(page)

        if not search_box:
            raise Exception("Could not find search box with any known selector")

        search_box.scroll_into_view_if_needed()
        time.sleep(0.5)
        search_box.click()
        time.sleep(0.5)
        search_box.fill(search_query)
        time.sleep(0.5)
        search_box.press("Enter")
        time.sleep(5)

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
                    # Try multiple methods to get the website
                    website_link = page.locator('a[data-item-id="authority"]').first
                    if website_link.count() > 0:
                        website = website_link.get_attribute('href')

                        # If href is empty or invalid, try getting the visible text
                        if not website or website.strip() == "":
                            website_text = website_link.inner_text()
                            if website_text and ('.' in website_text):
                                website = website_text

                    # Fallback: look for any link with "Website" text nearby
                    if not website:
                        website_links = page.locator('a:has-text("Website"), a[aria-label*="Website"]').all()
                        if len(website_links) > 0:
                            website = website_links[0].get_attribute('href')
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


def try_click_service_dropdowns(page, verbose=False):
    """Try to click on service-related dropdowns/menus to reveal hidden content."""
    revealed_text = ""

    # Common selectors for service dropdowns/menus
    service_selectors = [
        'a:has-text("Services")',
        'button:has-text("Services")',
        'a:has-text("What We Do")',
        'button:has-text("What We Do")',
        'a:has-text("Products")',
        'button:has-text("Products")',
        '[aria-label*="Services"]',
        '[aria-label*="Menu"]',
    ]

    for selector in service_selectors:
        try:
            element = page.locator(selector).first
            if element.count() > 0 and element.is_visible(timeout=1000):
                # Try to hover/click to reveal dropdown
                element.hover(timeout=2000)
                time.sleep(0.5)

                # Get any revealed content
                try:
                    dropdown_content = page.locator('nav, .dropdown, .menu, [role="menu"]').all_inner_texts()
                    revealed_text += ' '.join(dropdown_content)
                except:
                    pass

                break  # Only click the first one we find
        except:
            continue

    return revealed_text


def try_visit_service_pages(page, base_url, verbose=False):
    """Try to find and visit service-related pages to get more content."""
    all_text = ""

    # Common service page patterns
    service_page_patterns = [
        'services',
        'what-we-do',
        'products',
        'solutions',
        'our-services',
        'commercial-services',
    ]

    # First, try to find links on the current page
    service_links = []
    for pattern in service_page_patterns:
        try:
            links = page.locator(f'a[href*="{pattern}"]').all()
            for link in links[:2]:  # Only check first 2 matches per pattern
                try:
                    href = link.get_attribute('href')
                    if href and href not in service_links:
                        service_links.append(href)
                except:
                    pass
        except:
            continue

    # Visit each service link (max 2 to keep it fast)
    for link in service_links[:2]:
        try:
            # Make link absolute if it's relative
            if link.startswith('/'):
                link = base_url.rstrip('/') + link
            elif not link.startswith('http'):
                link = base_url.rstrip('/') + '/' + link

            if verbose:
                print(f"            🔍 Checking: {link[:40]}...")

            page.goto(link, timeout=15000, wait_until='domcontentloaded')
            time.sleep(1)

            page_text = page.inner_text('body')
            all_text += ' ' + page_text

        except Exception as e:
            if verbose:
                print(f"            ⚠️  Couldn't load service page: {str(e)[:40]}")
            continue

    return all_text


def classify_lead_tier(company, page, verbose=True):
    """Classify a lead into Tier 1, 2, or 3 with enhanced multi-page checking."""
    company_name = company.get('Company Name', 'Unknown')
    website = company.get('Website', '')

    if not website or website.strip() == "":
        if verbose:
            print(f"      ℹ️  {company_name[:40]}: No website → Tier 2")
        return "Tier 2", [], []

    # Show raw URL for debugging
    if verbose:
        print(f"      📋 {company_name[:40]}: Raw URL: {website[:60]}")

    # Clean and validate URL before attempting to visit
    cleaned_url = clean_url(website)

    if not cleaned_url:
        if verbose:
            print(f"      ⚠️  {company_name[:40]}: Invalid URL format → Tier 3")
        return "Tier 3", [], []

    try:
        if verbose:
            if cleaned_url != website:
                print(f"      🧹 {company_name[:40]}: Cleaned to: {cleaned_url[:60]}")
            print(f"      🌐 {company_name[:40]}: Checking {cleaned_url[:50]}...")

        # Random delay to avoid detection
        time.sleep(random.uniform(2, 4))

        # Try to visit the website with longer timeout (using cleaned URL)
        page.goto(cleaned_url, timeout=20000, wait_until='domcontentloaded')
        time.sleep(2)

        # Get homepage text
        page_text = page.inner_text('body')

        # Try to click service dropdowns to reveal hidden content
        try:
            dropdown_text = try_click_service_dropdowns(page, verbose=verbose)
            if dropdown_text:
                page_text += ' ' + dropdown_text
        except:
            pass

        # Try to visit service pages for more content
        try:
            service_page_text = try_visit_service_pages(page, cleaned_url, verbose=verbose)
            if service_page_text:
                page_text += ' ' + service_page_text
        except:
            pass

        # Extract emails and check for keywords from ALL collected text
        emails = extract_emails(page_text)
        keywords_found = check_for_keywords(page_text)

        if keywords_found:
            if verbose:
                print(f"         ✅ TIER 1! Found keywords: {', '.join(keywords_found[:3])}")
            return "Tier 1", keywords_found, emails
        else:
            if verbose:
                print(f"         📄 Tier 3 (website loads but no keywords)")
            return "Tier 3", [], emails

    except Exception as e:
        error_msg = str(e)[:100]
        # Better error handling - don't let 403/timeout stop the whole script
        if verbose:
            if '403' in error_msg or 'Forbidden' in error_msg:
                print(f"         ⚠️  Tier 3 (403 Forbidden - site blocking us)")
            elif 'Timeout' in error_msg or 'timeout' in error_msg:
                print(f"         ⚠️  Tier 3 (timeout - site too slow)")
            elif 'net::' in error_msg:
                print(f"         ⚠️  Tier 3 (connection error)")
            else:
                print(f"         ⚠️  Tier 3 (couldn't load website: {error_msg})")
        return "Tier 3", [], []


# ============================================================================
# MAIN SCRAPER FUNCTION
# ============================================================================

def scrape_texas_roofing_companies():
    """Main scraping function with city selection."""
    print("=" * 80)
    print("🏢 TEXAS ROOFING COMPANY LEAD GENERATOR - SINGLE CITY VERSION")
    print("=" * 80)
    print()
    print("Available cities:")
    cities = list(TEXAS_MARKETS.keys())
    for i, city in enumerate(cities, 1):
        zip_count = len(TEXAS_MARKETS[city])
        print(f"  {i}. {city} ({zip_count} zip codes)")

    print()
    print("=" * 80)
    print()

    # Get user choice
    while True:
        try:
            choice = input("Enter city number (1-5): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(cities):
                selected_city = cities[choice_num - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(cities)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nCancelled by user.")
            return

    zip_codes = TEXAS_MARKETS[selected_city]

    print()
    print("=" * 80)
    print(f"🎯 You selected: {selected_city.upper()}")
    print(f"📊 Will scan {len(zip_codes)} zip codes")
    print(f"⏱️  Expected runtime: {len(zip_codes) * 2} - {len(zip_codes) * 3} minutes")
    print("=" * 80)
    print()
    input("Press Enter to start scraping...")
    print()

    all_leads = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        print(f"\n🌆 Starting {selected_city.upper()}")
        print(f"   Scanning {len(zip_codes)} zip codes...\n")

        for zip_code in tqdm(zip_codes, desc=f"   {selected_city}", unit="zip"):
            print(f"\n   📍 Zip: {zip_code}")
            companies = scrape_google_maps_results(page, selected_city, zip_code)
            print(f"      Found {len(companies)} companies")

            for company in companies:
                if is_duplicate(company['Company Name'], company['Phone'], all_leads):
                    print(f"      ⏭️  {company['Company Name'][:40]}: Duplicate, skipping")
                    continue

                tier, keywords, emails = classify_lead_tier(company, page, verbose=True)

                company['Lead Tier'] = tier
                company['Keywords Found'] = ', '.join(keywords) if keywords else ''
                company['Email'] = ', '.join(emails) if emails else ''

                all_leads.append(company)

            time.sleep(1)

        print(f"\n   ✅ {selected_city} complete! Found {len(all_leads)} unique leads.")

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
        df = df.sort_values(['Lead Tier'])

        output_file = f'{selected_city.lower()}_roofing_leads.xlsx'
        df.to_excel(output_file, index=False, engine='openpyxl')

        print(f"✅ SUCCESS! Saved {len(all_leads)} unique leads to '{output_file}'")
        print(f"\n📊 LEAD BREAKDOWN:")
        print(f"   Tier 1 (High Value): {len([l for l in all_leads if l['Lead Tier'] == 'Tier 1'])}")
        print(f"   Tier 2 (Opportunity): {len([l for l in all_leads if l['Lead Tier'] == 'Tier 2'])}")
        print(f"   Tier 3 (Low Value): {len([l for l in all_leads if l['Lead Tier'] == 'Tier 3'])}")
    else:
        print("⚠️  No leads found. Please check your internet connection and try again.")

    print("=" * 80)
    print("🎉 Scraping complete!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        scrape_texas_roofing_companies()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        print("Please check the error message and try again.")
