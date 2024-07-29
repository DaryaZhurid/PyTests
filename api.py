import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import settings
import uuid


class Pets:
    """ API библиотека к сайту http://34.141.58.52:8080/#/"""

    def __init__(self):
        self.base_url = 'http://34.141.58.52:8000/'

    def get_registered(self) -> json:
        """Post-запрос к Swagger сайта для регистрации нового пользователя по указанным email и password"""
        e = uuid.uuid4().hex
        email = f'{e}@gmail.com'
        data = {"email": email,
                "password": settings.NEW_USER_PASSWORD, "confirm_password": settings.NEW_USER_PASSWORD}
        res = requests.post(self.base_url + 'register', data=json.dumps(data))
        user_token = res.json()['token']
        new_id = res.json()
        new_id = new_id.get('id')
        status = res.status_code
        return status, new_id, user_token

    def get_token(self) -> json:
        """Post-запрос к Swagger сайта для получения уникального токена пользователя по зарегистрированным email и
        password"""
        data = {"email": settings.VALID_EMAIL,
                "password": settings.VALID_PASSWORD}
        res = requests.post(self.base_url + 'login', data=json.dumps(data))
        my_token = res.json()['token']
        status = res.status_code
        my_id = res.json()['id']
        return my_token, status, my_id

    def get_list_users(self) -> json:
        """Get-запрос к Swagger сайта для получения списка пользователей по токен, полученному из функции get_token"""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + 'users', headers=headers)
        status = res.status_code
        list_users = res.text
        return status, list_users

    def post_pet_save(self) -> json:
        """Post-запрос к Swagger сайта для добавления нового питомца по токен, полученному из функции get_token"""
        my_token, _, my_id = Pets().get_token()
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {'name': 'John', 'type': 'dog', 'age': 5, 'owner_id': my_id}
        res = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        new_pet_id = res.json()['id']
        status = res.status_code
        return new_pet_id, status

    def post_pet_photo(self) -> json:
        """Post-запрос к Swagger сайта для добавления фото в карточку питомца"""
        my_token = Pets().get_token()[0]
        pet_id = Pets().post_pet_save()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        files = {'pic': (
            'John.jpg', open('tests\\photo\\pet_John.jpg', 'rb'), 'image/jpg')}
        res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
        status = res.status_code
        link = res.json()['link']
        return status, link

    def delete_another_user(self, user_id: int, my_token: str) -> json:
        """Delete-запрос к Swagger сайта для удаления пользователя по его id и чужому token"""
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {'id': user_id}
        res = requests.delete(self.base_url + f'users/{user_id}', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def delete_user(self, user_id: int, user_token: str) -> json:
        """Delete-запрос к Swagger сайта для удаления пользователя по id"""
        headers = {'Authorization': f'Bearer {user_token}'}
        data = {'id': user_id}
        res = requests.delete(self.base_url + f'users/{user_id}', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def get_pet_like(self) -> json:
        """Put-запрос к Swagger сайта для добавления лайка питомцу по id"""
        my_token, _, _ = Pets().get_token()
        pet_id, _ = Pets().post_pet_save()
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {'id': pet_id}
        res = requests.put(self.base_url + f'pet/{pet_id}/like', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def get_pets_list(self) -> json:
        """Post-запрос к Swagger сайта для получения списка питомцев по id"""
        my_token, _, my_id = Pets().get_token()
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {'user_id': my_id}
        res = requests.post(self.base_url + 'pets', data=json.dumps(data), headers=headers)
        status = res.status_code
        pets_list = res.text
        return status, pets_list

    def get_pet_comment(self) -> json:
        """Put-запрос к Swagger сайта для добавления комментария питомцу"""
        my_token, _, my_id = Pets().get_token()
        pet_id, _ = Pets().post_pet_save()
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {'message': settings.MESSAGE}
        res = requests.put(self.base_url + f'pet/{pet_id}/comment', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def pet_update(self) -> json:
        """Patch-запрос к Swagger сайта для редактирования данных питомца"""
        my_token, _, my_id = Pets().get_token()
        pet_id, _ = Pets().post_pet_save()
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {
            'id': pet_id,
            'name': settings.MESSAGE,
            'type': 'cat',
            'age': 9,
            'gender': 'male',
            'owner_id': my_id,
            'pic': 'string',
            'owner_name': settings.VALID_EMAIL
        }
        res = requests.patch(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def get_info_pet(self) -> json:
        """Get-запрос к Swagger сайта для получения информации о питомце"""
        my_token, _, _ = Pets().get_token()
        pet_id, _ = Pets().post_pet_save()
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + f'pet/{pet_id}', headers=headers)
        status = res.status_code
        list_pet_info = res.text
        return status, list_pet_info

    def delete_pet(self) -> json:
        """Delete-запрос к Swagger сайта для удаления питомца по id"""
        my_token, _, _ = Pets().get_token()
        pet_id, _ = Pets().post_pet_save()
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {'id': pet_id}
        res = requests.delete(self.base_url + f'pet/{pet_id}', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def delete_another_pet(self) -> json:
        """Delete-запрос к Swagger сайта для удаления питомца без регистрации"""
        pet_id, _ = Pets().post_pet_save()
        data = {'id': pet_id}
        res = requests.delete(self.base_url + f'pet/{pet_id}', data=json.dumps(data))
        status = res.status_code
        return status


Pets().get_registered()
Pets().get_token()
Pets().get_list_users()
Pets().post_pet_save()
Pets().post_pet_photo()
_, user_id_, user_token_ = Pets().get_registered()
my_token_, _, my_id_ = Pets().get_token()
Pets().delete_another_user(user_id_, my_token_)
Pets().delete_user(user_id_, user_token_)
Pets().get_pet_like()
Pets().get_pets_list()
Pets().get_pet_comment()
Pets().pet_update()
Pets().get_info_pet()
Pets().delete_pet()
Pets().delete_another_pet()
