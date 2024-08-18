import allure
import requests
from data_registration import DataUserRegistration
from urls import Urls


class TestsLoginUser:
    @allure.title('Логин с неверным логином и паролем')
    def test_login_not_exist_user(self):
        payload = {
            "email": "persik@yandex.ru",
            "password": "lalala123456!"
        }
        response = requests.post(f"{Urls.BASE_URL}/api/auth/login", data=payload)
        message = response.json()["message"]
        assert response.status_code == 401 and message == 'email or password are incorrect'

    @allure.title('Логин под существующим пользователем')
    def test_valid_login_user(self):
        payload = {
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD,
            "name": DataUserRegistration.NAME
        }
        requests.post(f"{Urls.BASE_URL}/api/auth/register", data=payload)
        response2 = requests.post(f"{Urls.BASE_URL}/api/auth/login", data={
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD
        })
        check_success_create_user = response2.json()["success"]
        token = response2.json()["accessToken"]
        assert response2.status_code == 200 and check_success_create_user is True
        # удаление пользователя
        requests.delete(f"{Urls.BASE_URL}/api/auth/user", headers={'Authorization': token})