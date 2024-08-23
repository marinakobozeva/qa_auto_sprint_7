import requests
import random
import string
from faker import Faker
from random import randint, choice


# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def generate_courier():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    return payload

def generate_order():
    fake = Faker()
    payload = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": f"{fake.street_name()}, {fake.building_number().replace('/', '')}",
        "metroStation": "Бульвар Рокоссовского",
        "phone": f"+7{randint(10**9, 10**10 - 1)}",
        "rentTime": randint(1, 5),
        "deliveryDate": fake.date(),
        "comment": "Saske, come back to Konoha",
        "color": [choice(["BLACK", "GREY"])],
    }
    return payload



