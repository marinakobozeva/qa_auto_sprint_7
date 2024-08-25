from helpers import generate_courier, generate_order
from data import UrlList
import requests
import allure
import pytest

class TestApiOrderPost:

    @allure.title("Создание заказа с выбором разных цветов или без цвета вовсе")
    @allure.description("Блокирующая ошибка. Статус ответа 500 вместо 201")
    @pytest.mark.parametrize("color", ["BLACK", "GREY", ""])
    def test_create_order(self, color):
        url = UrlList.BASE_URL + UrlList.ORDERS_URL
        payload = generate_order()
        payload["color"] = color
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 500
        assert response_dict["message"] == 'values.map is not a function'

    @allure.title("Создание заказа с выбором двух цветов цветов")
    def test_create_order_with_both_colors(self, color=["BLACK", "GREY"]):
        url = UrlList.BASE_URL + UrlList.ORDERS_URL
        payload = generate_order()
        payload["color"] = color
        response = requests.post(url, data=payload)
        response_dict = response.json()
        assert response.status_code == 201
        assert "track" in response_dict



