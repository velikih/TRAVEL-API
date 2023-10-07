import logging
from typing import Tuple, Union, List

from domain.interface import PerevalRepository, ImgRepo, UserRepo
from domain.dataclasses import BodyInfo, PerevalInfo


class MobileTourist:

	def __init__(
			self,
			pereval_repo: PerevalRepository,
			img_repo: ImgRepo,
			user_repo: UserRepo,
			logger: logging.Logger = logging.Logger('service_logger')
	):
		self.pereval_repo = pereval_repo
		self.img_repo = img_repo
		self.user_repo = user_repo
		self.logger = logger

	def add_data(self, body: BodyInfo) -> int:
		coords_id = self.pereval_repo.add_coords(body.coords.dict())

		level_id = self.pereval_repo.add_level(body.level.dict())

		user = self.user_repo.get_user_by_phone(body.user.phone)
		if user is None:
			user_id = self.user_repo.add_user(body.user.dict())
		else:
			user_id = user.id

		data_id = self.pereval_repo.add_data(
			data_for_add={
				'beauty_title': body.beauty_title,
				'title': body.title,
				'other_titles': body.other_titles,
				'connect': body.connect,
				'add_time': body.add_time,
				'user_id': user_id,
				'coords_id': coords_id,
				'level_id': level_id,
			}
		)

		for image in body.images:
			self.img_repo.add_image(
				{
					'img': image.img,
					'title': image.title,
					'pereval_id': data_id
				}
			)
		self.logger.info('User by user_id = %s added new data' % user_id)
		return data_id

	def edit_pereval_data(self, pereval_id: int, body: BodyInfo) -> Tuple[int, Union[str, None]]:
		old_pereval = self.pereval_repo.get_pereval(pereval_id=pereval_id)
		if old_pereval is None:
			return 0, 'No pereval with id %s' % pereval_id
		if old_pereval.status is True:
			return 0, 'Pereval has already been approved'

		user = self.user_repo.get_user_by_phone(body.user.phone)
		if user is None or user.email != body.user.email or\
					user.name != body.user.name or\
					user.fam != body.user.fam or\
					user.otc != body.user.otc:
			return 0, 'Personal Data Error'

		self.pereval_repo.edit_pereval(
			pereval_id=pereval_id,
			pereval={
				'beauty_title': body.beauty_title,
				'title': body.title,
				'other_titles': body.other_titles,
				'connect': body.connect
			}
		)
		self.pereval_repo.edit_coords(coords_id=old_pereval.coords_id, coords=body.coords.dict())
		self.pereval_repo.edit_levels(levels_id=old_pereval.level_id, levels=body.level.dict())
		self.img_repo.edit_imgs(
			pereval_id=pereval_id,
			images=[
				{
					'img': image.img,
					'title': image.title,
				} for image in body.images
			]
		)
		return 1, None


	def get_pereval_data(self, pereval_id: int) -> PerevalInfo:
		pereval = self.pereval_repo.get_pereval(pereval_id=pereval_id)
		images = self.img_repo.get_imgs_by_pereval_id(pereval_id=pereval.id)
		coords = self.pereval_repo.get_coords_by_id(coords_id=pereval.coords_id)
		user = self.user_repo.get_user_by_id(user_id=pereval.user_id)
		levels = self.pereval_repo.get_levels_by_id(level_id=pereval.level_id)
		return PerevalInfo(
			beauty_title=pereval.beauty_title,
			title=pereval.title,
			other_titles=pereval.other_titles,
			connect=pereval.connect,
			add_time=pereval.add_time,
			user={
				'email': user.email,
				'fam': user.fam,
				'name': user.name,
				'otc': user.otc,
				'phone': user.phone
			},
			coords={
				'latitude': coords.latitude,
				'longitude': coords.longitude,
				'height': coords.height
			},
			level={
				'winter': levels.winter,
				'summer': levels.summer,
				'autumn': levels.autumn,
				'spring': levels.spring
			},
			images=[
				{
					'img': image.img,
					'title': image.title,
				} for image in images
			],
			status=pereval.status
		)
