import logging

from domain.interface import Repository
from domain.dataclasses import BodyInfo, PerevalInfo, ImageInfo, CoordsInfo, UserInfo, LevelInfo


class MobileTourist:
	def __init__(
			self,
			repository: Repository,
			logger: logging.Logger = logging.Logger('service_logger')
	):
		self.repo = repository
		self.logger = logger

	def add_data(self, body: BodyInfo) -> int:
		coords_id = self.repo.add_coords(body.coords.dict())

		level_id = self.repo.add_level(body.level.dict())

		user = self.repo.get_user_by_phone(body.user.phone)
		if user is None:
			user_id = self.repo.add_user(body.user.dict())
		else:
			user_id = user.id

		data_id = self.repo.add_data(
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
			self.repo.add_image(
				{
					'img': image.img,
					'title': image.title,
					'pereval_id': data_id
				}
			)
		self.logger.info('User by user_id = %s added new data' % user_id)
		return data_id

	def get_pereval_data(self, pereval_id: int) -> BodyInfo:
		pereval = self.repo.get_pereval(pereval_id=pereval_id)
		images = self.repo.get_imgs_by_pereval_id(pereval_id=pereval.id)
		coords = self.repo.get_coords_by_id(coords_id=pereval.coords_id)
		user = self.repo.get_user_by_id(user_id=pereval.user_id)
		levels = self.repo.get_levels_by_id(level_id=pereval.level_id)
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

