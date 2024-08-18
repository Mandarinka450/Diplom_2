import requests
from data_registration import DataUserRegistration
from urls import Urls
import allure


class TestsCreateUser:
    @allure.title('Создание нового пользователя')
    def test_create_new_user(self):
        payload = {
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD,
            "name": DataUserRegistration.NAME
        }
        response1 = requests.post(f"{Urls.BASE_URL}/api/auth/register", data=payload)
        check_success_create_user = response1.json()["success"]
        assert response1.status_code == 200 and check_success_create_user is True
        # удаление пользователя
        response2 = requests.post(f"{Urls.BASE_URL}/api/auth/login", data={
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD
        })
        token = response2.json()["accessToken"]
        requests.delete(f"{Urls.BASE_URL}/api/auth/user", headers={'Authorization': token})

    @allure.title('Создание нового пользователя с незаполненным одним из обязательных параметров')
    def test_create_user_without_needed_parameter(self):
        payload = {
            "password": DataUserRegistration.PASSWORD,
            "name": DataUserRegistration.NAME
        }
        response = requests.post(f"{Urls.BASE_URL}/api/auth/register", data=payload)
        message = response.json()["message"]
        assert response.status_code == 403 and message == 'Email, password and name are required fields'

    @allure.title('Создание уже зарегистрированного пользователя')
    def test_create_exist_user(self):
        payload = {
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD,
            "name": DataUserRegistration.NAME
        }
        requests.post(f"{Urls.BASE_URL}/api/auth/register", data=payload)
        response = requests.post(f"{Urls.BASE_URL}/api/auth/register", data=payload)
        message = response.json()["message"]
        assert response.status_code == 403 and message == 'User already exists'
        # удаление пользователя
        response2 = requests.post(f"{Urls.BASE_URL}/api/auth/login", data={
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD
        })
        token = response2.json()["accessToken"]
        requests.delete(f"{Urls.BASE_URL}/api/auth/user", headers={'Authorization': token})
