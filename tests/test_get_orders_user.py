import allure
import requests

from data_user import DataUser
from urls import Urls


class TestsGetOrdersUser:
    @allure.title('Получение заказа авторизованного пользователя')
    def test_get_orders_user_with_login(self):
        response = requests.post(f"{Urls.BASE_URL}/api/auth/login", data={
            "email": DataUser.EMAIL,
            "password": DataUser.PASSWORD
        })
        token = response.json()["accessToken"]
        response_get_orders = requests.get(f"{Urls.BASE_URL}/api/orders", headers={'Authorization': token})
        check_success_get_orders = response_get_orders.json()["success"]
        assert response_get_orders.status_code == 200 and check_success_get_orders is True

    @allure.title('Получение заказа под неавторизованным пользователем')
    def test_get_orders_user_without_login(self):
        response_get_orders = requests.get(f"{Urls.BASE_URL}/api/orders")
        message_success_get_orders = response_get_orders.json()["message"]
        assert response_get_orders.status_code == 401 and message_success_get_orders == 'You should be authorised'
