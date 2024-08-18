import allure
import requests
from data_registration import DataUserRegistration
from urls import Urls


class TestsEditDataUser:
    @allure.title('Изменение поля name пользователя без авторизации')
    def test_edit_name_data_user_without_login(self):
        response = requests.patch(f"{Urls.BASE_URL}/api/auth/user", data={
            "name": "Кукуку"
        })
        message = response.json()["message"]
        assert response.status_code == 401 and message == 'You should be authorised'

    @allure.title('Изменение поля email пользователя без авторизации')
    def test_edit_email_data_user_without_login(self):
        response = requests.patch(f"{Urls.BASE_URL}/api/auth/user", data={
            "email": 'pechenka205@mail.su',
        })
        message = response.json()["message"]
        assert response.status_code == 401 and message == 'You should be authorised'

    @allure.title('Изменение поля name авторизованного пользователя')
    def test_edit_name_data_user_with_authorize(self):
        expected_name = 'Анастасия мандарин'
        # Создание пользователя
        payload = {
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD,
            "name": DataUserRegistration.NAME
        }
        requests.post(f"{Urls.BASE_URL}/api/auth/register", data=payload)
        # Логин пользователя
        response = requests.post(f"{Urls.BASE_URL}/api/auth/login", data={
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD
        })
        token = response.json()["accessToken"]
        # Редактирование данных
        requests.patch(f"{Urls.BASE_URL}/api/auth/user", data={
            "name": expected_name
        }, headers={'Authorization': token})
        response2 = requests.get(f"{Urls.BASE_URL}/api/auth/user", headers={'Authorization': token})
        actual_name = response2.json()['user']['name']
        assert actual_name == expected_name
        # Удаление пользователя
        requests.delete(f"{Urls.BASE_URL}/api/auth/user", headers={'Authorization': token})

    @allure.title('Изменение поля email авторизованного пользователя')
    def test_edit_email_data_user_with_authorize(self):
        expected_email = 'pechenka120@mail.ru'
        # Создание пользователя
        payload = {
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD,
            "name": DataUserRegistration.NAME
        }
        requests.post(f"{Urls.BASE_URL}/api/auth/register", data=payload)
        # Логин пользователя
        response = requests.post(f"{Urls.BASE_URL}/api/auth/login", data={
            "email": DataUserRegistration.EMAIL,
            "password": DataUserRegistration.PASSWORD
        })
        token = response.json()["accessToken"]
        # Редактирование данных
        requests.patch(f"{Urls.BASE_URL}/api/auth/user", data={
            "email": expected_email
        }, headers={'Authorization': token})
        response2 = requests.get(f"{Urls.BASE_URL}/api/auth/user", headers={'Authorization': token})
        actual_email = response2.json()['user']['email']
        assert actual_email == expected_email
        # Удаление пользователя
        requests.delete(f"{Urls.BASE_URL}/api/auth/user", headers={'Authorization': token})
