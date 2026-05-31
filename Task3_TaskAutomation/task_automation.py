"""
CodeAlpha Internship — Task 3: Task Automation with Python Scripts
==================================================================
All three automation ideas combined in one menu-driven script:
  1. Move all .jpg files from one folder to another.
  2. Extract email addresses from a .txt file → save to new file.
  3. Scrape the title of a fixed webpage and save it.
Key Concepts: os, shutil, re, requests, file handling.
"""

import os
import re
import shutil

# ─────────────────────────────────────────────────────────
#  TASK 3A — Move .jpg files to a destination folder
# ─────────────────────────────────────────────────────────
def move_jpg_files():
    print("\n  ── Automation 1: Move .jpg Files ──────────────────────")

    src = input("  Source folder path (press Enter for current dir): ").strip()
    if not src:
        src = os.getcwd()

    dst = input("  Destination folder (press Enter for './moved_images'): ").strip()
    if not dst:
        dst = os.path.join(os.getcwd(), "moved_images")

    if not os.path.isdir(src):
        print(f"  ⚠  Source folder not found: {src}")
        return

    os.makedirs(dst, exist_ok=True)

    jpg_files = [f for f in os.listdir(src)
                 if f.lower().endswith(".jpg") and os.path.isfile(os.path.join(src, f))]

    if not jpg_files:
        print(f"  ℹ  No .jpg files found in '{src}'.")
        return

    moved = 0
    for filename in jpg_files:
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)

        # Avoid overwriting: rename if file already exists
        if os.path.exists(dst_path):
            base, ext = os.path.splitext(filename)
            dst_path  = os.path.join(dst, f"{base}_copy{ext}")

        shutil.move(src_path, dst_path)
        print(f"  ✅  Moved: {filename}")
        moved += 1

    print(f"\n  📦  {moved} file(s) moved to: {os.path.abspath(dst)}")


# ─────────────────────────────────────────────────────────
#  TASK 3B — Extract email addresses from a .txt file
# ─────────────────────────────────────────────────────────
def extract_emails():
    print("\n  ── Automation 2: Extract Email Addresses ──────────────")

    src_file = input("  Path to source .txt file: ").strip()
    if not os.path.isfile(src_file):
        print(f"  ⚠  File not found: {src_file}")
        return

    out_file = input("  Save emails to (press Enter for 'extracted_emails.txt'): ").strip()
    if not out_file:
        out_file = "extracted_emails.txt"

    with open(src_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Regex pattern — matches standard email addresses
    email_pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    emails = sorted(set(re.findall(email_pattern, content)))

    if not emails:
        print("  ℹ  No email addresses found in the file.")
        return

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"Extracted Email Addresses ({len(emails)} found)\n")
        f.write("=" * 45 + "\n")
        for email in emails:
            f.write(email + "\n")

    print(f"\n  ✅  {len(emails)} unique email(s) saved to: {os.path.abspath(out_file)}")
    for email in emails:
        print(f"      → {email}")


# ─────────────────────────────────────────────────────────
#  TASK 3C — Scrape webpage title and save it
# ─────────────────────────────────────────────────────────
def scrape_webpage_title():
    print("\n  ── Automation 3: Scrape Webpage Title ─────────────────")

    try:
        import requests
    except ImportError:
        print("  ⚠  'requests' library not installed. Run: pip install requests")
        return

    # Fixed URL as per task scope
    url = "https://www.wikipedia.org"
    out_file = "scraped_titles.txt"

    print(f"  🌐  Fetching title from: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  ❌  Failed to fetch page: {e}")
        return

    # Extract <title> tag using regex (no external HTML parser needed)
    match = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.IGNORECASE | re.DOTALL)
    title = match.group(1).strip() if match else "Title not found"

    print(f"  📌  Page title: {title}")

    # Append to file (so multiple runs accumulate results)
    with open(out_file, "a", encoding="utf-8") as f:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}]  URL: {url}\n")
        f.write(f"               Title: {title}\n")
        f.write("-" * 55 + "\n")

    print(f"  💾  Title saved to: {os.path.abspath(out_file)}")


# ─────────────────────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 55)
    print("   🤖  TASK AUTOMATION SCRIPTS  —  CodeAlpha Task 3")
    print("=" * 55)

    menu = {
        "1": ("Move .jpg files to a new folder",          move_jpg_files),
        "2": ("Extract emails from a .txt file",          extract_emails),
        "3": ("Scrape webpage title and save it",         scrape_webpage_title),
        "4": ("Run ALL three automations",                None),
        "0": ("Exit",                                     None),
    }

    while True:
        print("\n  Choose an automation task:")
        for key, (label, _) in menu.items():
            print(f"    [{key}]  {label}")

        choice = input("\n  Your choice: ").strip()

        if choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        elif choice == "1":
            move_jpg_files()
        elif choice == "2":
            extract_emails()
        elif choice == "3":
            scrape_webpage_title()
        elif choice == "4":
            move_jpg_files()
            extract_emails()
            scrape_webpage_title()
        else:
            print("  ⚠  Invalid choice. Please enter 0–4.")


if __name__ == "__main__":
    main()
