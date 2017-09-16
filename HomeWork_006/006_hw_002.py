import datetime

CURRENT_YEAR = 2017

class Book:
    def __init__(self, in_name, in_author, in_year):
        if in_year > CURRENT_YEAR:
            raise ValueError('Книга не может быть из будущего!')
        self.name = in_name
        self.author = in_author
        self.year = in_year
        self.reviews = []

    def __str__(self):
        return f'Книга "{self.name}", автор {self.author}, издана в {self.year} году'

    def __eq__(self, other):
        if self.author == other.author and self.name == other.name and self.year == other.year:
            return True
        return False

    def add_review(self, in_author, in_text):
        self.reviews.append({'date': datetime.datetime.now(), 'author': in_author, 'text': in_text})

    def show_reviews(self):
        print(f'На данную книгу оставлено {len(self.reviews)} отзывов:')
        for i in self.reviews:
            print('*'*50)
            print(f'* Отзыв оставлен {i["date"].strftime("%d.%m.%Y %H:%M:%S")}, читателем {i["author"]}:')
            print('*'*50)
            print(i['text'])
            print('*'*50)
            print()



def main():
    book1 = Book('Звёздные войны, эпизод 1', 'Терри Брукс', 1999)
    book2 = Book('Звёздные войны, эпизод 1', 'Терри Брукс', 1999)
    book3 = Book('Звёздные войны, эпизод 2', 'Роберт Сальватор', 2002)

    print(book1 == book2)
    print(book1 == book3)
    print()

    print(book1)
    book1.add_review('DobrijZmej', 'Интересно, но без остальных книг, не входящих в эпизоды, теряет смысл')
    book1.add_review('Некто', 'Фильм так себе')
    book1.show_reviews()




if __name__ == '__main__':
    main()