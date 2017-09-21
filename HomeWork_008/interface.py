from storage import Storage

def main():
    storage1 = Storage()

    storage1.add('some.url', 'some_user', 'some_pass')
    storage1.add('second.url', 'DobrijZmej', '******')
    storage1.add('other.url', 'DobrijZmej1', '******')
    storage1.get_all()

    print(storage1.get('some.url'))

    storage1.erase('second.url')
    storage1.get_all()
    storage1.erase('second.url')

if __name__ == '__main__':
    main()