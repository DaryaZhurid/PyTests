import pytest
from api import Pets

pet = Pets()


@pytest.mark.smoke
def test_get_registered():
    status = pet.get_registered()[0]
    new_id = pet.get_registered()[1]
    user_token = pet.get_registered()[2]
    assert status == 200
    assert new_id
    assert user_token


@pytest.mark.smoke
def test_get_token():
    my_token = pet.get_token()[0]
    status = pet.get_token()[1]
    my_id = pet.get_token()[2]
    assert my_token
    assert status == 200
    assert my_id


@pytest.mark.regression
def test_list_users():
    status = pet.get_list_users()[0]
    list_users = pet.get_list_users()[1]
    assert status == 200
    assert list_users


@pytest.mark.smoke
def test_post_pet_save():
    new_pet_id, status = pet.post_pet_save()
    assert new_pet_id
    assert status == 200


@pytest.mark.smoke
def test_post_pet_photo():
    status = pet.post_pet_photo()[0]
    link = pet.post_pet_photo()[1]
    assert status == 200
    assert link


@pytest.mark.regression
def test_delete_another_user():
    status, user_id, user_token = pet.get_registered()
    my_token, _, _ = pet.get_token()
    delete_status = pet.delete_another_user(user_id, my_token)
    assert delete_status == 403


@pytest.mark.regression
def test_delete_user():
    status, user_id, user_token = pet.get_registered()
    delete_status = pet.delete_user(user_id, user_token)
    assert delete_status == 200


@pytest.mark.xfail
def test_get_pet_like():
    status = pet.get_pet_like()
    assert status == 403, 'Баг Swagger'


@pytest.mark.smoke
def test_get_pets_list():
    status = pet.get_pets_list()[0]
    pets_list = pet.get_pets_list()[1]
    assert status == 200
    assert pets_list


@pytest.mark.regression
@pytest.mark.xfail
def test_get_pet_comment():
    status = pet.get_pet_comment()
    assert status == 200, (f'Нет возможности через swagger создать комментарий, '
                           f'поэтому берется существующий (см. текст к функции в файле api)')


@pytest.mark.regression
def test_pet_update():
    status = pet.pet_update()
    assert status == 200


@pytest.mark.smoke
def test_get_info_pet():
    status = pet.get_info_pet()[0]
    list_pet_info = pet.get_info_pet()[1]
    assert status == 200
    assert list_pet_info


@pytest.mark.smoke
def test_delete_pet():
    status = pet.delete_pet()
    assert status == 200


@pytest.mark.regression
def test_delete_another_pet():
    status = pet.delete_another_pet()
    assert status == 403
