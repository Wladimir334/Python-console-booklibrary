
from . import Book

class Library:

    def __init__(self, storage):
        self.books = {}
        self.storage = storage
        self.last_id = None

    def _get_last_id_book(self):
        last_id = self.storage.get_last_id()
        return last_id

    def increment_book_id(self):
        self.last_id = int(self._get_last_id_book())
        self.last_id += 1
        self.storage.increment_last_id()

    def add_book(self, book):
        if isinstance(book, Book):
            self.increment_book_id()
            book.id = str(self.last_id)
            self.storage.write_data(book.to_dict())
            return book
        raise ValueError("Неверный формат книги!")

    # def get_book_info(self, book_id):
    #     return self.books.get(book_id)

    def get_book_by_id(self, book_id):
        book = self.books.get(book_id)
        if book:
            return
        raise ValueError("Такой книги нет")

    def get_book_by_isbn(self, isbn):
        results = []
        books = self.storage.read_data()
        for item in books:
            if isbn.lower() in item['ISBN'].lower():
                results.append(Book.from_dict(item))
        return results

    def get_books_by_author(self, author):
        results = []
        books = self.storage.read_data()
        for item in books:
            if author.lower() in item['author'].lower():
                    results.append(Book.from_dict(item))
        return results

    def get_books_by_title(self, title):
        books = {}
        for id_, book in self.books.items():
            if title.lower() in book.title.lower():
                books[id_] = book
            return books

    def get_books(self):
        books = self.storage.read_data()
        books_obj = []
        for book in books:
            books_obj.append(Book.from_dict(book))
        return books

    def search_book(self, query):
        results = {}
        for id_, book in self.books.items():
            if query.lower() in book.author.lower():
                results[id_] = book
        return results

    def book_delete(self, isbn: str):
        # получаем список словарей
        books = self.storage.read_data()
        # проходимсся по списку словарей и
        for i, book in enumerate(books):
            # удаляем словарь с нужным isbngit
            if book['ISBN'].lower() == isbn.lower():
                books.pop(i)
        # очищаем файл (начиная с конца хедера (33))
        self.storage.file.seek(33)
        self.storage.file.truncate()
        # добавляем заново книги из словаря в файл,
        # перед этим преобразуя в объект Book
        for book in books:
            self.add_book(Book.from_dict(book))


    def get_book_count(self):
        pass

    def check_book(self, isbn):
        books = self.storage.read_data()
        for item in books:
            if item['ISBN'].lower() == isbn.lower():
                return item['ISBN']
        return None

    def dump_books_data(self, filename):
        self.storage.dump_books_to_json(filename)
