import allure
import requests
from data_user import DataUser
from urls import Urls


class TestsCreateOrder:
    @allure.title('Создание заказа под авторизованным пользователем и с ингредиентами')
    def test_create_order_with_login_user_with_ingredients(self):
        response = requests.post(f"{Urls.BASE_URL}/api/auth/login", data={
            "email": DataUser.EMAIL,
            "password": DataUser.PASSWORD
        })
        token = response.json()["accessToken"]
        response_ingredients = requests.post(f"{Urls.BASE_URL}/api/orders", json={
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f", "61c0c5a71d1f82001bdaaa72"]
        }, headers={'Authorization': token})
        check_success_create_order = response_ingredients.json()["success"]
        assert response_ingredients.status_code == 200 and check_success_create_order is True

    @allure.title('Оформление заказа под неавторизованным пользователем')
    def test_create_order_without_login_user(self):
        response_ingredients = requests.post(f"{Urls.BASE_URL}/api/orders", json={
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa70", "61c0c5a71d1f82001bdaaa79"]
        })
        check_success_create_order = response_ingredients.json()["success"]
        assert response_ingredients.status_code == 200 and check_success_create_order is True

    @allure.title('Оформление заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        response_ingredients = requests.post(f"{Urls.BASE_URL}/api/orders", json={
            "ingredients": []
        })
        message_error_create_order = response_ingredients.json()["message"]
        assert response_ingredients.status_code == 400 and message_error_create_order == 'Ingredient ids must be provided'

    @allure.title('Оформление заказа с неверным хешем ингредиента')
    def test_create_order_with_invalid_hash_of_ingredient(self):
        response_ingredients = requests.post(f"{Urls.BASE_URL}/api/orders", json={
            "ingredients": ["dddd777", "61c0c5a71d1f82001bdaaa70", "61c0c5a71d1f82001bdaaa79"]
        })
        assert response_ingredients.status_code == 500
