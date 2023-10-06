import logging

from domain.interface import Repository
from domain.dataclasses import BodyInfo


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
