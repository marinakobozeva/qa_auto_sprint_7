from helpers import generate_courier, generate_order
from data import UrlList
import requests
import pytest
import allure


class TestApiPost:

    @allure.title("Регистрация курьера с валидными данными")
    def test_create_curier(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        response = requests.post(url, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Регистрация курьеров с одинаковыми данными")
    def test_same_couriers_not_registred(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        response_1 = requests.post(url, data=payload)
        response_2 = requests.post(url, data=payload)
        response_2_dict = response_2.json()
        assert response_2.status_code == 409
        assert "message" in response_2_dict

    @allure.title("Регистрация курьера без ввода пароля")
    def test_create_courier_without_password(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        payload["password"] = ""
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 400
        assert "message" in response_dict

    @allure.title("Регистрация курьера без ввода логина")
    def test_create_courier_without_login(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload = generate_courier()
        payload["login"] = ""
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 400
        assert "message" in response_dict

    @allure.title("Регистрация курьера с повторяющимся логином")
    def test_create_courier_with_same_login(self):
        url = UrlList.BASE_URL + UrlList.SING_UP_URL
        payload_1 = generate_courier()
        response = requests.post(url, data=payload_1)
        payload_2 = generate_courier()
        payload_2["login"] = payload_1["login"]
        response = requests.post(url, data=payload_2)
        response_dict = response.json()
        assert response.status_code == 409
        assert "message" in response_dict

    @allure.title("Вход курьера с валидными данными")
    def test_sing_in_courier(self):
        sign_up_url = UrlList.BASE_URL + UrlList.SING_UP_URL
        sign_in_url = UrlList.BASE_URL + UrlList.SING_IN_URL
        payload = generate_courier()
        sign_up_response = requests.post(sign_up_url, data=payload)
        del payload["firstName"]
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        assert sign_in_response.status_code == 200
        assert len(sign_in_response_dict) == 1
        assert "id" in sign_in_response_dict
        assert isinstance(sign_in_response_dict["id"], int)

    @allure.title("Вход курьера без ввода логина")
    def test_sign_in_courier_without_login(self):
        sign_up_url = UrlList.BASE_URL + UrlList.SING_UP_URL
        sign_in_url = UrlList.BASE_URL + UrlList.SING_IN_URL
        payload = generate_courier()
        sign_up_response = requests.post(sign_up_url, data=payload)
        del payload["firstName"]
        payload["login"] = ""
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        assert sign_in_response.status_code == 400
        assert "message" in sign_in_response_dict
        assert sign_in_response_dict["message"] == "Недостаточно данных для входа"

    @allure.title("Вход курьера без ввода пароля")
    def test_sign_in_courier_without_password(self):
        sign_up_url = UrlList.BASE_URL + UrlList.SING_UP_URL
        sign_in_url = UrlList.BASE_URL + UrlList.SING_IN_URL
        payload = generate_courier()
        sign_up_response = requests.post(sign_up_url, data=payload)
        del payload["firstName"]
        payload["password"] = ""
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        assert sign_in_response.status_code == 400
        assert "message" in sign_in_response_dict
        assert sign_in_response_dict["message"] == "Недостаточно данных для входа"

    @allure.title("Вход курьера с неверным  паролем")
    def test_sign_in_courier_wrong_password(self):
        sign_up_url = UrlList.BASE_URL + UrlList.SING_UP_URL
        sign_in_url = UrlList.BASE_URL + UrlList.SING_IN_URL
        payload = generate_courier()
        sign_up_response = requests.post(sign_up_url, data=payload)
        del payload["firstName"]
        payload["password"] = "12345"
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        assert sign_in_response.status_code == 404
        assert "message" in sign_in_response_dict
        assert sign_in_response_dict["message"] == "Учетная запись не найдена"

    @allure.title("Вход курьера с неверным  логином")
    def test_sign_in_courier_wrong_login(self):
        sign_up_url = UrlList.BASE_URL + UrlList.SING_UP_URL
        sign_in_url = UrlList.BASE_URL + UrlList.SING_IN_URL
        payload = generate_courier()
        sign_up_response = requests.post(sign_up_url, data=payload)
        del payload["firstName"]
        payload["login"] = "dog"
        sign_in_response = requests.post(sign_in_url, data=payload)
        sign_in_response_dict = sign_in_response.json()
        assert sign_in_response.status_code == 404
        assert "message" in sign_in_response_dict
        assert sign_in_response_dict["message"] == "Учетная запись не найдена"

    @allure.title("Создание заказа с выбором разных цветов или без цвета вовсе")
    @allure.description("Блокирующая ошибка. Статус ответа 500 вместо 201")
    @pytest.mark.parametrize("color", ["BLACK", "GREY", ""])
    def test_create_order(self, color):
        url = UrlList.BASE_URL + UrlList.ORDERS_URL
        payload = generate_order()
        payload["color"] = color
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code != 201
        assert "message" in response_dict

    @allure.title("Создание заказа с выбором двух цветов цветов")
    def test_create_order_with_both_colors(self, color=["BLACK", "GREY"]):
        url = UrlList.BASE_URL + UrlList.ORDERS_URL
        payload = generate_order()
        payload["color"] = color
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 201
        assert "track" in response_dict



