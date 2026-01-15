# 🏢 Texas Roofing Company Lead Generator

A Python-based web scraper that automatically finds and qualifies roofing companies across major Texas cities using an intelligent **Tiered Lead Quality System**.

---

## 🎯 What This Script Does

This scraper searches Google Maps for roofing companies in 5 major Texas cities, then visits their websites to classify them into quality tiers based on their services.

### The Tiered System:

- **Tier 1 (🌟 High Value):** Companies with websites that mention specialized roofing keywords (silicone coating, roof restoration, elastomeric, etc.)
- **Tier 2 (🔧 Opportunity):** Companies without websites (potential clients for digital services)
- **Tier 3 (📄 Standard):** Companies with websites but no specialized keywords

---

## 📊 Features

✅ **Pre-configured Texas Markets:** Houston, Dallas, Austin, San Antonio, Fort Worth
✅ **150+ Zip Codes:** Top 20-30 zip codes per city already included
✅ **Automated Classification:** Visits websites and scans for 13 specialized roofing keywords
✅ **Smart Deduplication:** Prevents the same company from appearing multiple times
✅ **Email Extraction:** Automatically finds emails from company websites
✅ **Progress Tracking:** Real-time progress bars so you know it's working
✅ **Error Handling:** Won't crash if one website fails to load
✅ **Anti-Ban Protection:** Random delays (3-7 seconds) between requests
✅ **Excel Export:** Clean, organized output with all data in one file

---

## 🚀 Quick Start (Windows)

### 1. Install Python
Download from https://www.python.org/downloads/
**Important:** Check "Add Python to PATH" during installation!

### 2. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Run the Script
```bash
python texas_roofing_scraper.py
```

### 4. Get Your Results
Open `texas_roofing_leads.xlsx` when complete!

**📖 For detailed step-by-step instructions, see [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)**

---

## 📋 Output Format

The script generates `texas_roofing_leads.xlsx` with these columns:

| Column | Description |
|--------|-------------|
| **City** | Houston, Dallas, Austin, San Antonio, or Fort Worth |
| **Lead Tier** | Tier 1, Tier 2, or Tier 3 |
| **Company Name** | Business name |
| **Phone** | Phone number |
| **Email** | Email address (if found) |
| **Website** | Company website URL |
| **Keywords Found** | Specialized roofing keywords detected |
| **Address** | Physical address |
| **Zip Code Used** | Which zip code search found this company |

---

## ⚙️ Customization

### Add More Cities

Edit the `TEXAS_MARKETS` dictionary in `texas_roofing_scraper.py`:

```python
TEXAS_MARKETS = {
    "Houston": ["77002", "77003", ...],
    "Dallas": ["75201", "75202", ...],
    # Add your city here:
    "El Paso": ["79901", "79902", "79903"],
}
```

### Add More Zip Codes

Just append to any city's list:

```python
"Houston": [
    "77002", "77003", "77004",  # existing
    "77098", "77099",  # add new ones here
],
```

### Modify Target Keywords

Edit the `TARGET_KEYWORDS` list:

```python
TARGET_KEYWORDS = [
    "fluid applied",
    "silicone coating",
    "your custom keyword",  # add here
]
```

---

## ⏱️ Expected Runtime

- **Full run (5 cities, ~150 zip codes):** 2-4 hours
- **Test run (1 city, 5 zip codes):** ~15-20 minutes

The script intentionally runs slowly (3-7 second delays) to avoid being blocked by Google.

---

## 🛡️ Anti-Detection Features

- Random delays between requests (3-7 seconds)
- Real browser fingerprint (using Playwright)
- Proper User-Agent headers
- Realistic scrolling behavior
- Avoids suspicious patterns

---

## 🐛 Common Issues & Solutions

### "python is not recognized"
→ Reinstall Python with "Add to PATH" checked

### Script runs but finds no leads
→ Check your internet connection
→ Try increasing timeout values in the script

### Too slow / taking forever
→ Reduce zip codes for testing
→ Run overnight for full scan

### Getting blocked by Google
→ Don't run multiple times per day
→ Increase delay times if needed

**See [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) for full troubleshooting guide**

---

## 📦 Project Structure

```
Webscraper/
│
├── texas_roofing_scraper.py      # Main script
├── requirements.txt               # Python dependencies
├── WINDOWS_SETUP_GUIDE.md        # Detailed setup instructions
├── README_ROOFING_SCRAPER.md     # This file
└── texas_roofing_leads.xlsx      # Output file (generated after run)
```

---

## 🎓 How It Works

1. **Loop Through Cities:** Iterates through each city in TEXAS_MARKETS
2. **Loop Through Zip Codes:** For each city, searches each zip code
3. **Scrape Google Maps:** Finds roofing companies for that location
4. **Extract Basic Info:** Gets name, phone, address, website from Maps
5. **Visit Websites:** Goes to each company's website (if they have one)
6. **Scan for Keywords:** Looks for specialized roofing terms
7. **Extract Emails:** Uses regex to find email addresses
8. **Classify Tier:** Assigns Tier 1, 2, or 3 based on findings
9. **Check Duplicates:** Prevents same company from appearing twice
10. **Export to Excel:** Saves all results in organized spreadsheet

---

## 💡 Pro Tips

- **Start Small:** Test with 1 city and 5 zip codes first
- **Run Overnight:** Full scans take hours - start before bed
- **Focus on Tier 1:** These are your highest-value leads
- **Tier 2 = Opportunity:** Companies without websites need digital services
- **Don't Over-Scrape:** Running too often may get you rate-limited

---

## 📜 Target Keywords (Tier 1 Classification)

Companies using these keywords are classified as Tier 1:

- fluid applied
- silicone coating
- acrylic coating
- roof restoration
- aluminum coating
- elastomeric
- polyurethane
- commercial roof coating
- liquid applied
- cool roof
- white roof
- waterproofing
- PMMA

---

## ⚖️ Ethical Use

This script is for **legitimate business lead generation only**:

✅ Finding potential business clients
✅ Market research
✅ Competitive analysis

❌ DO NOT use for spamming
❌ DO NOT scrape excessively
❌ DO NOT violate Google's Terms of Service

**Be respectful:** Add delays, don't overuse, and use data responsibly.

---

## 🤝 Support

If you encounter issues:

1. Check the [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) troubleshooting section
2. Verify all dependencies are installed: `pip list`
3. Test with reduced zip codes first
4. Make sure you have a stable internet connection

---

## 📄 License

This script is provided as-is for educational and business purposes.

---

**Happy Lead Hunting! 🎯**
