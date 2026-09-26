import os
import random

BOOKS_DIR = "books"

def get_random_quote():
    books = [f for f in os.listdir(BOOKS_DIR) if f.endswith(".txt")]
    if not books:
        raise Exception("No book files found in books/ folder")

    chosen_book = random.choice(books)
    book_name = chosen_book.replace(".txt", "").replace("_", " ").title()

    with open(os.path.join(BOOKS_DIR, chosen_book), "r", encoding="utf-8") as f:
        quotes = [line.strip() for line in f if line.strip()]

    if not quotes:
    # Return a default quote instead of throwing an error and breaking the pipeline
    return "Keep your face always toward the sunshine—and shadows will fall behind you.", "Fallback Inspiration"

    quote = random.choice(quotes)
    return quote, book_name

if __name__ == "__main__":
    quote, book = get_random_quote()
    print(f"Quote: {quote}")
    print(f"Book: {book}")

    with open("current_quote.txt", "w", encoding="utf-8") as f:
        f.write(f"{quote}\n{book}")
