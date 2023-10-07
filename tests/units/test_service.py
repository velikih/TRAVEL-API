from datetime import datetime

import pytest
from unittest.mock import Mock

from domain.service import MobileTourist
from domain.dataclasses import BodyInfo


body = BodyInfo(
	beauty_title='пер. ',
	title='Черкесия',
	other_titles='Рона',
	connect='Текстовое поле',
	add_time=datetime.utcnow(),
	user={
		'email': 'qwerty@mail.ru',
		'fam': 'Иванов',
		'name': 'Иван',
		'otc': 'Иванович',
		'phone': '+7 999 99 99'
	},
	coords={
		'latitude': 54.4656,
		'longitude': 9.4577,
		'height': 1500
	},
	level={
		'winter': '1A',
		'summer': '1А',
		'autumn': '1А',
		'spring': '2A',
	},
	images=[
		{
			'img': '\\x8534234568...',
			'title': 'Седловина'
		}
	]
)


@pytest.fixture(scope='function')
def mobile_tourist(pereval_repo, img_repo, user_repo):
	mobile_tourist = MobileTourist(
		pereval_repo=pereval_repo,
		img_repo=img_repo,
		user_repo=user_repo
	)
	return mobile_tourist


def test__add_data(mobile_tourist, pereval):
	new_id = mobile_tourist.add_data(body)

	mobile_tourist.pereval_repo.add_coords.assert_called_once()
	mobile_tourist.pereval_repo.add_level.assert_called_once()
	mobile_tourist.user_repo.get_user_by_phone.assert_called_once()
	mobile_tourist.pereval_repo.add_data.assert_called_once()
	mobile_tourist.img_repo.add_image.assert_called()
	assert new_id == pereval.id


def test__edit_pereval_data(mobile_tourist, pereval):
	status, message = mobile_tourist.edit_pereval_data(pereval_id=pereval.id, body=body)

	mobile_tourist.pereval_repo.get_pereval.assert_called_once()
	mobile_tourist.user_repo.get_user_by_phone.assert_called_once()
	mobile_tourist.pereval_repo.edit_pereval.assert_called_once()
	mobile_tourist.pereval_repo.edit_coords.assert_called_once()
	mobile_tourist.pereval_repo.edit_levels.assert_called_once()
	mobile_tourist.img_repo.edit_imgs.assert_called_once()

	assert status == 1
	assert message is None

	mobile_tourist.pereval_repo.get_pereval = Mock(return_value=None)
	status, message = mobile_tourist.edit_pereval_data(pereval_id=pereval.id, body=body)
	assert status == 0


def test__get_pereval_data(mobile_tourist, pereval):
	body_now = mobile_tourist.get_pereval_data(pereval_id=pereval.id)

	mobile_tourist.pereval_repo.get_pereval.assert_called_once()
	mobile_tourist.img_repo.get_imgs_by_pereval_id.assert_called_once()
	mobile_tourist.pereval_repo.get_coords_by_id.assert_called_once()
	mobile_tourist.user_repo.get_user_by_id.assert_called_once()
	mobile_tourist.pereval_repo.get_levels_by_id.assert_called_once()

	assert body_now.user == body.user
	assert body_now.title == body.title
