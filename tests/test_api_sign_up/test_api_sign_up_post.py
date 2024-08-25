from helpers import generate_courier, generate_order
from data import UrlList
import requests
import allure


class TestApiSignUpPost:

    @allure.title("Регистрация курьера с валидными данными")
    def test_create_curier(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        response = requests.post(url, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Регистрация курьеров с одинаковыми данными")
    @allure.description("Ожидаемый результат не совпадает с фактическим. Сообщение: 'Этот логин уже используется. Попробуйте другой.' вместо 'Этот логин уже используется. Также выводится код ответа 409'")
    def test_same_couriers_not_registred(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        response_1 = requests.post(url, data=payload)
        response_2 = requests.post(url, data=payload)
        response_2_dict = response_2.json()
        assert response_2.status_code == 409
        assert response_2_dict == {'code': 409, 'message': 'Этот логин уже используется. Попробуйте другой.'}

    @allure.title("Регистрация курьера без ввода пароля")
    @allure.description("Ожидаемый результат не совпадает с фактическим. Помимо сообщения выводится код отввета 400")
    def test_create_courier_without_password(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        payload["password"] = ""
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 400
        assert response_dict == {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}

    @allure.title("Регистрация курьера без ввода логина")
    @allure.description("Ожидаемый результат не совпадает с фактическим. Помимо сообщения выводится код отввета 400")
    def test_create_courier_without_login(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        payload["login"] = ""
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 400
        assert response_dict == {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}

    @allure.title("Регистрация курьера с повторяющимся логином")
    @allure.description("Ожидаемый результат не совпадает с фактическим. Сообщение: 'Этот логин уже используется. Попробуйте другой.' вместо 'Этот логин уже используется. Также выводится код ответа 409'")
    def test_create_courier_with_same_login(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload_1 = generate_courier()
        response = requests.post(url, data=payload_1)
        payload_2 = generate_courier()
        payload_2["login"] = payload_1["login"]
        response = requests.post(url, data=payload_2)
        response_dict = response.json()
        assert response.status_code == 409
        assert response_dict == {'code': 409, 'message': 'Этот логин уже используется. Попробуйте другой.'}