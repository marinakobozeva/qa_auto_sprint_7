from helpers import generate_courier, generate_order
from data import UrlList
import requests
import allure

class TestApiSignInPost:

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
    @allure.description("Ожидаемый результат не совпадает с фактическим. Помимо сообщения выводится код отввета 400")
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
        assert sign_in_response_dict == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @allure.title("Вход курьера без ввода пароля")
    @allure.description("Ожидаемый результат не совпадает с фактическим. Помимо сообщения выводится код отввета 400")
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
        assert sign_in_response_dict == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @allure.title("Вход курьера с неверным  паролем")
    @allure.description("Ожидаемый результат не совпадает с фактическим. Помимо сообщения выводится код отввета 404")
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
        assert sign_in_response_dict == {'code': 404, 'message': 'Учетная запись не найдена'}

    @allure.title("Вход курьера с неверным  логином")
    @allure.description("Ожидаемый результат не совпадает с фактическим. Помимо сообщения выводится код отввета 404")
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
        assert sign_in_response_dict == {'code': 404, 'message': 'Учетная запись не найдена'}
