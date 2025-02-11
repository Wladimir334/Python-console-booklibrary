from datetime import datetime
import uuid
from core.enums import GENRES


class Book:
    def __init__(self, title, author, year, genre):
        """
        Конструктор класса Book
        :param title:  Название книги
        :param author:  Автор книги
        :param year: Год книги
        :param genre:  Жанр книги (по умолчанию None)
        :param isbn:  Идентификационный номер книги (по умолчанию None)
        """

        self.id = None
        self.author = author
        self.title = title
        self.year = year
        self.genre = genre
        self.__isbn = uuid.uuid4().hex[:9]



    def get_info(self):
        """
        Возврщает строки с информацияей о книге
        :return: Строка с информацей о книге
        """
        info = f"{self.title} - {self. author} ({self.year})"
        if self.genre:
            info += f", Жанр: {self.genre}"
        info += f", ISBN: {self.__isbn}"
        return info

    @staticmethod
    def is_valid_year(year):
        if isinstance(year, int):
            if 1445 < year < datetime.today().year:
                return True
            else:
                return False
        elif isinstance(year, str):
            if year.isdigit():
                if 1445 < int(year) < datetime.today().year:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False



    def is_order_than(self, year):
        """
        Проверяет была ли книга издана до указанного года
        :param year: Год издания
        :return: bool
        """
        if self.is_valid_year(year):
            return self._year < year
        else:
            raise ValueError("Неверное значение для года издания!")

    @property
    def year(self):
        return self._year


    @year.setter
    def year(self, new_year):
        if self.is_valid_year(new_year):
            self._year = new_year
        else:
            raise ValueError("Неверное значение для года издания!")


    def get_book_age(self):
        current_year = datetime.today().year
        return current_year - self._year

    def to_dict(self):
        data = {"id": self.id,
                "author": self.author,
                "title": self.title,
                "year": self.year,
                "genre": self.genre,
                "ISBN": self.__isbn
                }
        return data
    @classmethod
    def from_dict(cls, book_data):
        book = Book(
            author=book_data["author"],
            title = book_data["title"],
            year = book_data["year"],
            genre = book_data["genre"]

        )
        book.isbn = book_data["ISBN"]
        book.id = book_data["id"]
        return book


    @property
    def genre(self):
        return self._genre


    @genre.setter
    def genre(self, genre):
        if genre.lower() in GENRES:
            self._genre = genre
        else:
            raise ValueError("Неизвестный жанр")

    @property
    def isbn(self):
        return self.__isbn

    @isbn.setter
    def isbn(self, isbn):
        self.__isbn = isbn



# book = Book(title="Капитанская дочка", author="Пушкин", year=1836, genre="роман")
#
# print(book.get_info)
# book.year = 1837
# print(book.year)
# print(book.get_book_age())
# print(book.is_order_than(year=1700))

