"""
Texas Roofing Company Lead Generator with Tiered Quality System
================================================================

This script scrapes roofing companies across major Texas cities and classifies
them into quality tiers based on their website content.

Tier 1: Has website + Contains specialized roofing keywords
Tier 2: No website (potential opportunity to offer digital services)
Tier 3: Has website but no specialized keywords

Author: Sales Automation Script
Date: 2026-01-15
"""

import re
import time
import random
from playwright.sync_api import sync_playwright
from tqdm import tqdm
import pandas as pd
from urllib.parse import urlparse

# ============================================================================
# TEXAS MARKETS DICTIONARY
# ============================================================================
# This dictionary contains major Texas cities and their top populated zip codes.
# You can easily add more cities or zip codes to expand your coverage.
#
# To add a new city:
# 1. Add a new key with the city name (e.g., "El Paso")
# 2. Add a list of zip codes for that city
# Example: "El Paso": ["79901", "79902", "79903", ...]
#
# To add more zip codes to an existing city:
# Just append them to the list for that city key
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

# ============================================================================
# KEYWORD LIST FOR TIER 1 CLASSIFICATION
# ============================================================================
# These keywords identify specialized roofing companies that work with
# advanced coating and restoration systems (high-value leads)
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
    """
    Extract email addresses from text using regex pattern.
    Returns a list of unique email addresses found.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return list(set(emails))  # Remove duplicates


def check_for_keywords(text):
    """
    Check if any target keywords appear in the text.
    Returns a list of keywords found (case-insensitive).
    """
    text_lower = text.lower()
    found_keywords = []

    for keyword in TARGET_KEYWORDS:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)

    return found_keywords


def clean_phone_number(phone):
    """
    Clean and standardize phone numbers.
    """
    if not phone:
        return ""
    # Remove common phone number formatting
    cleaned = re.sub(r'[^\d]', '', phone)
    return cleaned


def is_duplicate(company_name, phone, existing_leads):
    """
    Check if a lead already exists based on phone number or company name.
    This prevents the same company from appearing multiple times.
    """
    phone_cleaned = clean_phone_number(phone)

    for lead in existing_leads:
        existing_phone = clean_phone_number(lead.get('Phone', ''))
        existing_name = lead.get('Company Name', '').strip().lower()
        current_name = company_name.strip().lower()

        # Match by phone number (most reliable)
        if phone_cleaned and existing_phone and phone_cleaned == existing_phone:
            return True

        # Match by exact company name
        if current_name and existing_name and current_name == existing_name:
            return True

    return False


def scrape_google_maps_results(page, city, zip_code):
    """
    Scrape roofing companies from Google Maps for a specific city and zip code.
    Returns a list of company dictionaries with basic info.
    """
    search_query = f"Roofing company in {city} {zip_code}"
    companies = []

    try:
        # Navigate to Google Maps
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

        # Wait for search box to be available and visible
        search_box = page.locator('input[id="searchboxinput"]')
        search_box.wait_for(state="visible", timeout=10000)
        search_box.click()
        time.sleep(0.5)

        # Find search box and enter query
        search_box.fill(search_query)
        time.sleep(0.5)
        search_box.press("Enter")

        # Wait for results to load
        time.sleep(5)  # Increased wait time for results

        # Scroll through results to load more companies
        results_panel = page.locator('div[role="feed"]').first

        for _ in range(3):  # Scroll 3 times to load more results
            try:
                results_panel.evaluate("element => element.scrollBy(0, 1000)")
                time.sleep(1)
            except:
                pass

        # Extract company information
        result_items = page.locator('div[role="article"]').all()

        for item in result_items[:20]:  # Limit to first 20 results per zip
            try:
                # Extract company name
                name_elem = item.locator('div.fontHeadlineSmall').first
                company_name = name_elem.inner_text() if name_elem.count() > 0 else ""

                if not company_name:
                    continue

                # Click on the result to get more details
                item.click()
                time.sleep(1.5)

                # Extract phone number
                phone = ""
                try:
                    phone_button = page.locator('button[data-item-id*="phone"]').first
                    if phone_button.count() > 0:
                        phone_text = phone_button.get_attribute('data-item-id')
                        if phone_text:
                            phone = phone_text.split(':')[-1] if ':' in phone_text else ""
                except:
                    pass

                # Extract website
                website = ""
                try:
                    website_link = page.locator('a[data-item-id="authority"]').first
                    if website_link.count() > 0:
                        website = website_link.get_attribute('href')
                except:
                    pass

                # Extract address
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
                # Skip this company if there's an error
                continue

    except Exception as e:
        print(f"  ⚠️  Error scraping {city} {zip_code}: {str(e)}")

    return companies


def classify_lead_tier(company, page):
    """
    Classify a lead into Tier 1, 2, or 3 based on website content.

    Tier 1: Has website + Contains target keywords (HIGH VALUE)
    Tier 2: No website (OPPORTUNITY)
    Tier 3: Has website but no target keywords (LOW VALUE)

    Returns: tuple (tier, keywords_found, emails_found)
    """
    website = company.get('Website', '')

    # Scenario B: No website = Tier 2
    if not website or website.strip() == "":
        return "Tier 2", [], []

    # Scenario A: Has website - need to scrape it
    try:
        # Anti-ban measure: Random sleep between 3-7 seconds
        time.sleep(random.uniform(3, 7))

        # Visit the website
        page.goto(website, timeout=15000, wait_until='domcontentloaded')
        time.sleep(2)

        # Get all text content from the page
        page_text = page.inner_text('body')

        # Extract emails
        emails = extract_emails(page_text)

        # Check for target keywords
        keywords_found = check_for_keywords(page_text)

        # Determine tier
        if keywords_found:
            return "Tier 1", keywords_found, emails
        else:
            return "Tier 3", [], emails

    except Exception as e:
        # If website doesn't load, mark as Tier 3
        return "Tier 3", [], []


# ============================================================================
# MAIN SCRAPER FUNCTION
# ============================================================================

def scrape_texas_roofing_companies():
    """
    Main function that orchestrates the entire scraping process.
    """
    print("=" * 80)
    print("🏢 TEXAS ROOFING COMPANY LEAD GENERATOR")
    print("=" * 80)
    print(f"📍 Cities to scan: {', '.join(TEXAS_MARKETS.keys())}")
    print(f"📊 Total zip codes: {sum(len(zips) for zips in TEXAS_MARKETS.values())}")
    print("=" * 80)
    print()

    all_leads = []

    with sync_playwright() as p:
        # Launch browser (headless=False to see what's happening, set to True to hide)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        # Loop through each city
        for city, zip_codes in TEXAS_MARKETS.items():
            print(f"\n🌆 Starting {city.upper()}")
            print(f"   Scanning {len(zip_codes)} zip codes...\n")

            # Loop through each zip code with progress bar
            for zip_code in tqdm(zip_codes, desc=f"   {city}", unit="zip"):
                # Phase 1: Scrape Google Maps
                companies = scrape_google_maps_results(page, city, zip_code)

                # Phase 2: Classify each company (Tiered Logic)
                for company in companies:
                    # Check for duplicates before processing
                    if is_duplicate(company['Company Name'], company['Phone'], all_leads):
                        continue

                    # Classify the lead tier
                    tier, keywords, emails = classify_lead_tier(company, page)

                    # Add classification results to company data
                    company['Lead Tier'] = tier
                    company['Keywords Found'] = ', '.join(keywords) if keywords else ''
                    company['Email'] = ', '.join(emails) if emails else ''

                    # Add to master list
                    all_leads.append(company)

                # Small delay between zip codes
                time.sleep(1)

            print(f"   ✅ {city} complete! Found {len([l for l in all_leads if l['City'] == city])} unique leads.")

        browser.close()

    # Phase 3: Export to Excel
    print(f"\n{'=' * 80}")
    print(f"💾 Exporting results to Excel...")

    if all_leads:
        df = pd.DataFrame(all_leads)

        # Reorder columns for better readability
        column_order = [
            'City', 'Lead Tier', 'Company Name', 'Phone', 'Email',
            'Website', 'Keywords Found', 'Address', 'Zip Code Used'
        ]
        df = df[column_order]

        # Sort by City and Lead Tier
        df = df.sort_values(['City', 'Lead Tier'])

        # Export to Excel
        output_file = 'texas_roofing_leads.xlsx'
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
