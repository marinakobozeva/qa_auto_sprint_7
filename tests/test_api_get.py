from helpers import generate_courier, generate_order
from data import UrlList
import requests
import allure

class TestApiGet:
    @allure.title("Получение списка заказов курьера")
    def test_get_orders_list(self):
        url = UrlList.BASE_URL + UrlList.ORDERS_URL
        response = requests.get(url)
        response_dict = response.json()
        print(response_dict)
        assert response.status_code == 200
        assert "orders" in response_dict
        assert len(response_dict) == 3
        assert isinstance(response_dict["orders"], list)



