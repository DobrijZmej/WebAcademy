class Storage:
    def __init__(self):
        self.container = {}

    def add(self, in_url, in_login, in_pass):
        if in_url is None or in_url == '':
            raise ValueError('Адрес сайта не может быть пустым!')
        self.container[in_url.lower()] = [in_login, in_pass]

    def get(self, in_url):
        user_data = self.container[in_url.lower()]
        return f'{user_data[0]}/{user_data[1]}'

    def get_all(self):
        i = 1
        for url, user_data in self.container.items():
            print(f'{i}. {url}: {user_data[0]}/{user_data[1]}')
            i += 1

    def erase(self, in_url):
        if in_url.lower() in self.container.keys():
            del self.container[in_url.lower()]
        else:
            raise ValueError('Данных по этому сайту нет в базе!')

def main():
    storage = Storage()
    storage.add('me.ua', 'DobrijZmej', '123456')
    storage.add('me.ua2', 'DobrijZmej', '123456')
    storage.get_all()

    print(storage.get('me.ua'))

if __name__ == '__main__':
    main()