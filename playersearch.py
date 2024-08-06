import httpx
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime

# Define ANSI color codes
COLOR_GREEN = '\033[92m'  # Green color
COLOR_RESET = '\033[0m'   # Reset to default color

# List of URLs to capture
urls = [
    'https://cs2browser.com/gameserver/108840/geostrike-community-cs2-retake-geostrike-ge/',
    'https://cs2browser.com/gameserver/82346/geostrike-community-cs2-automix-geostrike-ge/',
    'https://cs2browser.com/gameserver/108840/geostrike-community-cs2-retake-geostrike-ge/',
    'https://cs2browser.com/gameserver/22374/geostrike-community-cs2-aim-geostrike-ge/'
]

# Function to fetch HTML content from a given URL
async def fetch_html(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

# Function to search for text in the HTML content
def search_text(html, search_term):
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.body(text=lambda t: search_term.lower() in t.lower())
    return search_results

# Function to get the current timestamp
def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Function to scan all URLs and print results
async def scan_urls(search_term):
    while True:
        print(f"\n[{get_timestamp()}] Starting a new scan...")

        for url in urls:
            print(f"[{get_timestamp()}] Fetching HTML content from {url}...")
            html = await fetch_html(url)
            results = search_text(html, search_term)
            
            # Determine the result of the search
            if results:
                print(f"{COLOR_GREEN}[{get_timestamp()}] Result: Found at {url}{COLOR_RESET}")
                print(f"{COLOR_GREEN}[{get_timestamp()}] Search term '{search_term}' found at {url}!{COLOR_RESET}")
                for result in results:
                    print(f"{COLOR_GREEN}[{get_timestamp()}] {result.strip()}{COLOR_RESET}")
            else:
                print(f"[{get_timestamp()}] Result: Not Found at {url}")

        # Wait for 5 seconds before the next scan
        await asyncio.sleep(5)

# Main function to start the script
async def main():
    # Prompt the user for a search term
    search_term = input("Enter the term you want to search for: ")
    
    # Start scanning URLs
    print(f"[{get_timestamp()}] Starting search for '{search_term}' across multiple URLs.")
    await scan_urls(search_term)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
