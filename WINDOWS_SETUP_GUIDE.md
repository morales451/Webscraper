# 🪟 Windows Setup Guide for Texas Roofing Scraper

## Complete Beginner-Friendly Setup Instructions

This guide will walk you through setting up and running the Texas Roofing Company scraper on Windows, even if you've never used Python before.

---

## Step 1: Install Python

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Click the yellow "Download Python 3.12.x" button (or latest version)

2. **Install Python:**
   - Run the downloaded installer
   - ⚠️ **IMPORTANT:** Check the box that says "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation:**
   - Press `Win + R` on your keyboard
   - Type `cmd` and press Enter
   - In the black window that opens, type:
     ```
     python --version
     ```
   - You should see something like `Python 3.12.1`
   - If you see an error, restart your computer and try again

---

## Step 2: Install Required Libraries

1. **Open Command Prompt:**
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to Your Script Folder:**
   - If your script is in `C:\Users\YourName\Documents\Webscraper`, type:
     ```
     cd C:\Users\YourName\Documents\Webscraper
     ```
   - Or simply open File Explorer, navigate to the folder containing the script, type `cmd` in the address bar, and press Enter

3. **Install Libraries:**
   - Copy and paste this command into Command Prompt:
     ```
     pip install playwright pandas openpyxl tqdm
     ```
   - Press Enter and wait (this may take 2-3 minutes)

4. **Install Playwright Browsers:**
   - After the above finishes, run:
     ```
     playwright install chromium
     ```
   - This downloads the browser that Playwright will use (may take 3-5 minutes)

---

## Step 3: Run the Script

1. **Make Sure You're in the Right Folder:**
   - In Command Prompt, you should be in the folder with `texas_roofing_scraper.py`
   - You can verify by typing `dir` and looking for the filename

2. **Run the Script:**
   ```
   python texas_roofing_scraper.py
   ```

3. **What to Expect:**
   - A Chrome browser window will open (this is normal!)
   - You'll see progress bars in the Command Prompt showing which city and zip code is being scanned
   - The script will say things like:
     ```
     🌆 Starting HOUSTON
        Scanning 30 zip codes...
     ```
   - **DO NOT CLOSE** the browser window or Command Prompt while it's running
   - The script will automatically close the browser when done

4. **How Long Does It Take?**
   - With 5 cities and ~30 zip codes each (150 total), expect:
     - **2-4 hours** for a complete run
     - The script sleeps 3-7 seconds between website visits to avoid being blocked
   - You can reduce the number of zip codes in the script to test faster

---

## Step 4: Find Your Results

1. **After the script finishes**, look in the same folder where the script is located

2. **You'll find a new file:**
   - `texas_roofing_leads.xlsx`

3. **Open it with Microsoft Excel or Google Sheets**

4. **Columns Explained:**
   - **City:** Which Texas city this lead is from
   - **Lead Tier:** Quality rating
     - **Tier 1** 🌟 = Has website + uses advanced roofing keywords (BEST LEADS)
     - **Tier 2** 🔧 = No website (opportunity to offer digital services)
     - **Tier 3** 📄 = Has website but no specialized keywords
   - **Company Name:** Business name
   - **Phone:** Phone number
   - **Email:** Email address (if found on their website)
   - **Website:** Company website URL
   - **Keywords Found:** Which special keywords were found (for Tier 1)
   - **Address:** Physical address
   - **Zip Code Used:** Which zip code search found this company

---

## Troubleshooting Common Issues

### ❌ "python is not recognized"
- **Solution:** You didn't check "Add Python to PATH" during installation
- **Fix:** Uninstall Python and reinstall, making sure to check the PATH box

### ❌ "pip is not recognized"
- **Solution:** Same as above - reinstall Python with PATH enabled

### ❌ Script stops with "TimeoutError"
- **Solution:** Your internet might be slow or Google Maps is loading slowly
- **Fix:** In the script, find `timeout=15000` and change to `timeout=30000`

### ❌ "ModuleNotFoundError: No module named 'playwright'"
- **Solution:** The libraries didn't install correctly
- **Fix:** Run the install commands again from Step 2

### ❌ Browser doesn't open
- **Solution:** Playwright browsers not installed
- **Fix:** Run `playwright install chromium` again

### ❌ Too many Tier 3 results, not enough Tier 1
- **Solution:** This is normal - most roofing companies don't use specialized coatings
- **Fix:** Focus on your Tier 1 leads (those are your gold!)

### ❌ Script is taking forever
- **Solution:** With ~150 zip codes and website visits, it's designed to take hours
- **Options:**
  - **Reduce zip codes:** Edit the script and use only 5-10 zip codes per city for testing
  - **Run overnight:** Start it before bed and check results in the morning
  - **Reduce sleep time:** Change `time.sleep(random.uniform(3, 7))` to `(2, 4)` (riskier - might get blocked)

---

## Customizing the Script

### Adding More Cities

1. Open `texas_roofing_scraper.py` in Notepad or any text editor
2. Find the `TEXAS_MARKETS` dictionary (around line 40)
3. Add a new city like this:

```python
TEXAS_MARKETS = {
    "Houston": [...],
    "Dallas": [...],
    # Add your new city here:
    "El Paso": ["79901", "79902", "79903", "79904", "79905"],
}
```

### Adding More Zip Codes to a City

```python
"Houston": [
    "77002", "77003", "77004",  # existing zips
    "77098", "77099", "77100",  # add new zips here
],
```

### Changing Keywords (for Tier 1 classification)

Find the `TARGET_KEYWORDS` list (around line 70) and add/remove keywords:

```python
TARGET_KEYWORDS = [
    "fluid applied",
    "silicone coating",
    # Add your own keywords:
    "spray foam",
    "TPO roofing",
]
```

### Running Headless (Hide the Browser)

Find this line (around line 400):
```python
browser = p.chromium.launch(headless=False)
```

Change to:
```python
browser = p.chromium.launch(headless=True)
```

---

## Tips for Best Results

1. **Run During Off-Peak Hours:** Run the script late at night or early morning to avoid getting rate-limited by Google

2. **Start Small:** Test with 1 city and 5 zip codes first to make sure everything works

3. **Don't Run Too Often:** Google Maps might temporarily block you if you run this multiple times per day

4. **Focus on Tier 1 Leads:** These are companies already doing specialized roofing work - your best prospects

5. **Use Tier 2 for Different Pitch:** Companies without websites might need digital services (web design, SEO, etc.)

---

## Need Help?

If you get stuck:
1. Read the error message carefully - it usually tells you what's wrong
2. Check the Troubleshooting section above
3. Make sure you followed all steps exactly
4. Try running the script with just 1 city and 3 zip codes to test

---

## Quick Reference Commands

```bash
# Install everything at once
pip install playwright pandas openpyxl tqdm
playwright install chromium

# Run the script
python texas_roofing_scraper.py

# Check if Python is installed
python --version

# Check if libraries are installed
pip list
```

---

**Good luck with your lead generation! 🚀**
