import httpx
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime
import re

# Define ANSI color codes
COLOR_GREEN = '\033[92m'  # Green color
COLOR_RESET = '\033[0m'   # Reset to default color

# Dictionary of URLs and their corresponding server names and IPs/Ports
urls = {
    'https://cs2browser.com/gameserver/21545/geostrike-community-cs2-public-geostrike-ge/': {
        'name': 'Public Server',
        'ip': '185.143.177.14:5555'
    },
    'https://cs2browser.com/gameserver/82346/geostrike-community-cs2-automix-geostrike-ge/': {
        'name': 'Automix Server',
        'ip': '185.143.177.14:4444'
    },
    'https://cs2browser.com/gameserver/108840/geostrike-community-cs2-retake-geostrike-ge/': {
        'name': 'Retake Server',
        'ip': '185.143.177.14:3333'
    },
    'https://cs2browser.com/gameserver/22374/geostrike-community-cs2-aim-geostrike-ge/': {
        'name': 'Aim Server',
        'ip': '185.143.177.14:6666'
    }
}

# Function to fetch HTML content from a given URL
async def fetch_html(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

# Function to search for text in the HTML content
def search_text(html, search_term):
    soup = BeautifulSoup(html, 'html.parser')
    search_pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    search_results = soup.body(text=lambda t: search_pattern.search(t))
    return search_results

# Function to get the current timestamp
def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Function to scan all URLs and print results
async def scan_urls(search_term):
    while True:
        print(f"\n[{get_timestamp()}] Starting a new scan...")

        for url, info in urls.items():
            server_name = info['name']
            server_ip = info['ip']
            print(f"[{get_timestamp()}] Fetching data from {server_name}...")
            html = await fetch_html(url)
            results = search_text(html, search_term)
            
            # Determine the result of the search
            if results:
                print(f"{COLOR_GREEN}[{get_timestamp()}] Result: Found at {server_name} ({server_ip}){COLOR_RESET}")
                for result in results:
                    print(f"{COLOR_GREEN}[{get_timestamp()}] {result.strip()}{COLOR_RESET}")
            else:
                print(f"[{get_timestamp()}] Result: Not Found at {server_name}")

        # Wait for 5 seconds before the next scan
        await asyncio.sleep(5)

# Main function to start the script
async def main():
    # Prompt the user for a search term
    search_term = input("Enter the Username you want to search for: ")
    
    # Start scanning URLs
    print(f"[{get_timestamp()}] Starting search for '{search_term}' across all Geostrike servers:")
    await scan_urls(search_term)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
