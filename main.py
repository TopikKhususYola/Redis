"""Simple Redis-backed book catalog display.

Run a Redis server locally (default port 6379), then:
    python main.py

It will store a list of books in Redis and then read them back and print them.
"""

from dataclasses import dataclass
from typing import Dict

import redis


@dataclass
class Book:
    title: str
    author: str
    year: int
    genre: str
    isbn: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "author": self.author,
            "year": str(self.year),
            "genre": self.genre,
            "isbn": self.isbn,
        }

    @classmethod
    def from_dict(cls, data: Dict[bytes, bytes]) -> "Book":
        # Redis returns bytes values; decode them to strings.
        decoded = {k.decode(): v.decode() for k, v in data.items()}
        return cls(
            title=decoded.get("title", ""),
            author=decoded.get("author", ""),
            year=int(decoded.get("year", "0")),
            genre=decoded.get("genre", ""),
            isbn=decoded.get("isbn", ""),
        )


REDIS_KEY_BASE = "book"


def main() -> None:
    # 1) Connect to Redis (localhost:6379 by default)
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=False)

    # 2) Create the book data you want to store
    books = [
        Book(title="Laskar Pelangi", author="Andrea Hirata", year=2005, genre="Sastra", isbn="9789791221070"),
        Book(title="Sebuah Seni untuk Bersikap Bodo Amat", author="Mark Manson", year=2016, genre="Pengembangan Diri", isbn="9781781258362"),
        Book(title="Atomic Habits", author="James Clear", year=2018, genre="Pengembangan Diri", isbn="9780735211292"),
        Book(title="Bumi", author="Tere Liye", year=2013, genre="Fantasi", isbn="9786024246603"),
        Book(title="Rich Dad Poor Dad", author="Robert T. Kiyosaki", year=1997, genre="Bisnis", isbn="9781612680194"),
    ]

    # 3) Store each book in Redis (as a hash)
    for idx, book in enumerate(books, start=1):
        key = f"{REDIS_KEY_BASE}:{idx}"
        r.hset(key, mapping=book.to_dict())

    # 4) Read them back from Redis and print
    print("Katalog buku dari Redis:")
    for idx in range(1, len(books) + 1):
        key = f"{REDIS_KEY_BASE}:{idx}"
        stored = r.hgetall(key)
        loaded_book = Book.from_dict(stored)

        print(f"\n-- Buku #{idx} --")
        print(f"Judul   : {loaded_book.title}")
        print(f"Penulis : {loaded_book.author}")
        print(f"Tahun   : {loaded_book.year}")
        print(f"Genre   : {loaded_book.genre}")
        print(f"ISBN    : {loaded_book.isbn}")


if __name__ == "__main__":
    main()
