import httpx
from bs4 import BeautifulSoup
import asyncio

# Define the URL you want to capture
url = 'https://cs2browser.com/gameserver/108840/geostrike-community-cs2-retake-geostrike-ge/'

# Function to fetch HTML content
async def fetch_html():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

# Function to search for text in the HTML content
def search_text(html, search_term):
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.body(text=lambda t: search_term.lower() in t.lower())
    return search_results

# Run the fetch function and parse the HTML
html = asyncio.run(fetch_html())

# Print the HTML content (pretty-printed for better readability)
print("Captured HTML content:")
print(BeautifulSoup(html, 'html.parser').prettify())

# Search for a specific term in the captured HTML
search_term = 'GeoStrike'  # Define the term you want to search for
results = search_text(html, search_term)

print(f"\nSearch results for '{search_term}':")
if results:
    for result in results:
        print(result)
else:
    print(f"No results found for '{search_term}'.")
