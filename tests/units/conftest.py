from unittest.mock import Mock

import pytest
from domain import interface


@pytest.fixture(scope="function")
def user_repo(user):
    user_repo = Mock(interface.UserRepo)
    user_repo.add_user = Mock(return_value=user.id)
    user_repo.get_user_by_phone = Mock(return_value=user)
    user_repo.get_user_by_id = Mock(return_value=user)
    return user_repo


@pytest.fixture(scope="function")
def img_repo(img):
    img_repo = Mock(interface.ImgRepo)
    img_repo.add_image = Mock(return_value=img.id)
    img_repo.get_imgs_by_pereval_id = Mock(return_value=[img])
    img_repo.edit_imgs = Mock(return_value=None)
    return img_repo


@pytest.fixture(scope="function")
def pereval_repo(pereval, pereval_info_response, coords, user, level):
    pereval_repo = Mock(interface.PerevalRepository)
    pereval_repo.add_data = Mock(return_value=pereval.id)
    pereval_repo.add_coords = Mock(return_value=coords.id)
    pereval_repo.add_level = Mock(return_value=level.id)
    pereval_repo.get_pereval = Mock(return_value=pereval)
    pereval_repo.get_coords_by_id = Mock(return_value=coords)
    pereval_repo.get_levels_by_id = Mock(return_value=level)
    pereval_repo.edit_pereval = Mock(return_value=None)
    pereval_repo.edit_coords = Mock(return_value=None)
    pereval_repo.edit_levels = Mock(return_value=None)
    pereval_repo.get_data_by_email = Mock(return_value=pereval_info_response)
    return pereval_repo
