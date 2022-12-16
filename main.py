from collections import UserDict



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
                return True
        return False

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

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
         
    def get_all_record(self):
        return self.data
    
    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name) -> Record:
        return self.data.get(name)

    def search(self, value):
        if self.has_record(value):
            return self.get_record(value)
    
    def remove_record(self, name):
        del self.data[name]

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
    name, phones = create_data(contact)

    if name in contacts:
        raise ValueError('This contact already exist.')
    record = Record(name)

    for phone in phones:
        record.add_phone(phone)

    contacts.add_record(record)
    return f'You added new contact: {name} and telephone number {phones}.'

@input_error
def change_contact(number):
    name, phones = create_data(number)
    record = contacts[name]
    record.change_phone(phones)
    return f'You changed contact'

@input_error
def show_phone(command_string):
    command, name = command_string.split(' ')
    number = contacts.search(name).search_phone()
    return number

def show_all(list_new):
    list_contacts = ''
    for key, record in contacts.get_all_record().items():
        list_contacts += f'{record.search_phone()}\n'
    
    return list_contacts

@input_error
def del_func(command_string):
    command, name = command_string.strip().split(' ')
    contacts.remove_record(name)
    return "You deleted the contact."


@input_error
def del_phone(data):
    command_fist, command_second, name, phone = data.strip().split(' ')
    record = contacts[name]
    if record.delete_phone(phone):
        return f'Phone {phone} for {name} contact deleted.'
    return f'{name} contact does not have this number'

def finish(end):
    exit()  

dict_command = {'hello': greeting,
    'add': add_contacts,
    'change': change_contact,
    'delete phone': del_phone,
    'delete': del_func,
    'phone': show_phone,
    'show all': show_all,
    'good bye': finish,
    'close': finish,
    'exit': finish
}

def create_data(data):
    """
    Розділяє вхідні дані на дві частини - номер і телефон.
    Також ці данні проходять валідацію.
    Для подальшої роботи з ними.
    :param data: Строка з номером і ім'ям.
    :return: Вже розділені ім'я і номер
    """
    command, name, *phones = data.strip().split(' ')

    if name.isnumeric() or name == '':
        raise ValueError('Wrong name. The name is number or you enter two space')
    for phone in phones:
        if not phone.isnumeric():
            raise ValueError('Wrong phones.')
    return name, phones

"""
Парсер команд.
Частина, яка відповідає за розбір введених користувачем рядків, 
виділення з рядка ключових слів та модифікаторів команд.
"""
def parser_command(command: str)->str:
    new_command = command.casefold()
    for key, action in dict_command.items():
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
        if action == 'exit' or action == 'good bye' or action == 'close':
            print ('Good bye!')
        result = parser_command(action)
        print(result)


if __name__ == '__main__':
    main()