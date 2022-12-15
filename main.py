from collections import UserDict

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[Record.name.value] = record
        return self.data[Record.name.value]

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for number in self.phones:
            if number.value == phone:
                self.phones.remove(number)
                return self.phones

    def change_phone(self, old_phone, new_phone):
        for number in self.phones:
            if number.value == old_phone:
                self.delete_phone(old_phone)
                self.add_phone(new_phone)
        return self.phones
    
    def search_phone(self):
        user_phones = []
        for phone in self.phones:
            user_phones.append(phone.value)
        return f'{self.name.value} : {user_phones}'

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass    

contacts = AddressBook()

"""
Декоратор винятків.
"""
def input_error(func):
    def miss_name(command):
        try:
            res = func(command)
            if res == None:
                return 'Enter user name. The first letter is capital, and the rest are small.'
            return res
        except (KeyError, IndexError):
            return 'Give your name and phone number, please!'   
    return miss_name
    
""" 
Функції обробники команд — handler, що відповідають
за безпосереднє виконання команд. 
"""
def greeting(word):
    return 'How can I help you?'


@input_error
def add_contacts(contact):
    add_contact = contact.split(' ') 
    contacts.update({add_contact[1]: add_contact[2]})
    return f'You add name {add_contact[1]} and telephone number {add_contact[2]}'

@input_error
def change_contact(number):
    new_number = number.split(' ')
    contacts[new_number[1]] = new_number[2]
    return f'You change contact of {new_number[1]}'

@input_error
def show_phone(name):
    new_name = name.split(' ')
    number = contacts.get(new_name[1])
    return number


def show_all(list_new):
    return contacts


def finish(end):
    exit()  

dict_command = {'hello': greeting,
    'add': add_contacts,
    'change': change_contact,
    'phone': show_phone,
    'show all': show_all,
    'good bye': finish,
    'close': finish,
    'exit': finish
}

"""
Парсер команд.
Частина, яка відповідає за розбір введених користувачем рядків, 
виділення з рядка ключових слів та модифікаторів команд.
"""
def parser_command(command: str)->str:

    for key, action in dict_command.items():
        new_command = command.casefold()
        if new_command.find(key) >= 0:
            return action(command)
    return 'You input wrong command! Please, try again'


"""
Цикл запит-відповідь. Ця частина програми відповідає за отримання від користувача даних та 
повернення користувачеві відповіді від функції-handlerа.
"""
def main():
    while True:
        action = input("Please, input your command...") 
        if 'exit' or 'good bye' or 'close':
            print ('Good bye!')
        result = parser_command(action)
        print(result)


if __name__ == '__main__':
    main()