import urllib.request
import json
import os

# Target file path inside the books folder
FILE_PATH = os.path.join("books", "meditations.txt")

def fetch_quotes():
    """Fetches quotes from ZenQuotes API and saves them into books/meditations.txt."""
    url = "https://zenquotes.io/api/quotes"
    
    # Ensure the books directory exists
    os.makedirs("books", exist_ok=True)
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            quotes_data = json.loads(response.read().decode())
            
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                for item in quotes_data:
                    quote = item.get("q")
                    author = item.get("a")
                    # Format as: "Quote text" - Author
                    f.write(f'"{quote}" - {author}\n')
            
            print(f"Successfully saved {len(quotes_data)} quotes to {FILE_PATH}")
            
    except Exception as e:
        print(f"Error fetching quotes: {e}")

if __name__ == "__main__":
    fetch_quotes()
