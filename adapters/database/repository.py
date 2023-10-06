from datetime import datetime, date
from typing import Optional, Dict, List, Any, Union

from sqlalchemy import (
	MetaData,
	DateTime,
	Date,
	Boolean,
	Integer,
	Unicode,
	Column,
	ForeignKey,
	Table,
	Float,
	insert,
	select,
	update,
	delete,
	func,
)
from sqlalchemy.orm import registry

from domain import interface, dataclasses

metadata = MetaData()
mapper = registry(metadata=metadata)

users = Table(
	'users',
	mapper.metadata,
	Column('id', Integer, primary_key=True),
	Column('email', Unicode(255), nullable=True),
	Column('fam', Unicode(255), nullable=False),
	Column('name', Unicode(255), nullable=False),
	Column('otc', Unicode(255), nullable=True),
	Column('phone', Unicode(255), nullable=False),
)

coords = Table(
	'coords',
	mapper.metadata,
	Column('id', Integer, primary_key=True),
	Column('latitude', Float, nullable=False),
	Column('longitude', Float, nullable=False),
	Column('height', Integer, nullable=False),
)

levels = Table(
	'levels',
	mapper.metadata,
	Column('id', Integer, primary_key=True),
	Column('winter', Unicode(255), nullable=False),
	Column('summer', Unicode(255), nullable=False),
	Column('autumn', Unicode(255), nullable=False),
	Column('spring', Unicode(255), nullable=False),
)

images = Table(
	'images',
	mapper.metadata,
	Column('id', Integer, primary_key=True),
	Column('img', Unicode, nullable=False),
	Column('title', Unicode(255), nullable=False),
	Column('pereval_id', Integer, ForeignKey('pereval_added.id'), nullable=False),
	Column('date_added', Date, server_default=func.now()),
)

pereval_added = Table(
	'pereval_added',
	mapper.metadata,
	Column('id', Integer, primary_key=True),
	Column('date_added', Date, server_default=func.now()),
	Column('beauty_title', Unicode(255), nullable=False),
	Column('title', Unicode(255), nullable=False),
	Column('other_titles', Unicode(255), nullable=False),
	Column('connect', Unicode(255), nullable=False),
	Column('add_time', DateTime, default=datetime.utcnow()),
	Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
	Column('coords_id', Integer, ForeignKey('coords.id'), nullable=False),
	Column('level_id', Integer, ForeignKey('levels.id'), nullable=False),
	Column('status', Boolean, default=False),
)

pereval_areas = Table(
	'pereval_areas',
	mapper.metadata,
	Column('id', Integer, primary_key=True),
	Column('id_parent', Integer, nullable=False),
	Column('title', Integer, nullable=False),
)

spr_activities_types = Table(
	'spr_activities_types',
	mapper.metadata,
	Column('id', Integer, primary_key=True),
	Column('title', Integer, nullable=False),
)


mapper.map_imperatively(dataclasses.User, users)
mapper.map_imperatively(dataclasses.Coords, coords)
mapper.map_imperatively(dataclasses.Level, levels)
mapper.map_imperatively(
	dataclasses.PerevalAdded,
	pereval_added
)

mapper.map_imperatively(
	dataclasses.Image,
	images
)


class Repository(interface.Repository):
	def __init__(self, engine):
		self.engine = engine

	def add_data(self, data_for_add: Dict) -> int:
		query = insert(dataclasses.PerevalAdded, data_for_add)
		result = self.engine.execute(query)
		return result.inserted_primary_key[0]

	def add_user(self, user: Dict) -> int:
		query = insert(dataclasses.User, user)
		result = self.engine.execute(query)
		return result.inserted_primary_key[0]

	def add_coords(self, coords: Dict) -> int:
		query = insert(dataclasses.Coords, coords)
		result = self.engine.execute(query)
		return result.inserted_primary_key[0]

	def add_level(self, level: Dict) -> int:
		query = insert(dataclasses.Level, level)
		result = self.engine.execute(query)
		return result.inserted_primary_key[0]

	def add_image(self, image: Dict) -> int:
		query = insert(dataclasses.Image, image)
		result = self.engine.execute(query)
		return result.inserted_primary_key[0]

	def get_user_by_phone(self, user_phone: str) -> Optional[dataclasses.User]:
		query = select(dataclasses.User).where(dataclasses.User.phone == user_phone)
		row = self.engine.execute(query).one_or_none()
		return dataclasses.User(**row) if row is not None else None

	def get_pereval(self, pereval_id: int) -> Optional[dataclasses.PerevalAdded]:
		query = select(dataclasses.PerevalAdded).where(dataclasses.PerevalAdded.id == pereval_id)
		row = self.engine.execute(query).one_or_none()
		return dataclasses.PerevalAdded(**row) if row is not None else None

	def get_imgs_by_pereval_id(self, pereval_id: int) -> List[dataclasses.Image]:
		query = select(dataclasses.Image).where(dataclasses.Image.pereval_id == pereval_id)
		rows = self.engine.execute(query).all()
		return [dataclasses.Image(**row) for row in rows]

	def get_coords_by_id(self, coords_id: int) -> Optional[dataclasses.Coords]:
		query = select(dataclasses.Coords).where(dataclasses.Coords.id == coords_id)
		row = self.engine.execute(query).one_or_none()
		return dataclasses.Coords(**row) if row is not None else None

	def get_user_by_id(self, user_id: int) -> Optional[dataclasses.User]:
		query = select(dataclasses.User).where(dataclasses.User.id == user_id)
		row = self.engine.execute(query).one_or_none()
		return dataclasses.User(**row) if row is not None else None

	def get_levels_by_id(self, level_id: int) -> Optional[dataclasses.Level]:
		query = select(dataclasses.Level).where(dataclasses.Level.id == level_id)
		row = self.engine.execute(query).one_or_none()
		return dataclasses.Level(**row) if row is not None else None

	def edit_pereval(self, pereval_id: int, pereval: Dict[str, str]) -> None:
		query = update(
			dataclasses.PerevalAdded
		).where(
			dataclasses.PerevalAdded.id == pereval_id
		).values(**pereval)
		self.engine.execute(query)

	def edit_imgs(self, pereval_id: int, images: List[Dict[str, Any]]) -> None:
		old_img_ids = self.engine.execute(
			select(dataclasses.Image.id).where(dataclasses.Image.pereval_id == pereval_id)
		).scalars().all()

		len_list_old_img = len(old_img_ids)

		for index_new_img in range(len(images)):
			if index_new_img < len_list_old_img:
				query = update(
					dataclasses.Image
				).where(
					dataclasses.Image.id == old_img_ids[index_new_img]
				).values(
					img=images[index_new_img]['img'],
					title=images[index_new_img]['title'],
					date_added=date.today()
				)
			else:
				query = insert(
					dataclasses.Image
				).values(
					img=images[index_new_img]['img'],
					title=images[index_new_img]['title'],
					pereval_id=pereval_id,
					date_added=date.today()
				)
			self.engine.execute(query)

		if not len(images):
			index_new_img = 0

		if len_list_old_img < index_new_img:
			for index in range(index_new_img, len_list_old_img):
				query = delete(
					dataclasses.Image
				).where(
					dataclasses.Image.id == old_img_ids[index]
				)
				self.engine.execute(query)

	def edit_coords(self, coords_id: int, coords: Dict[str, Union[float, int]]) -> None:
		query = update(
			dataclasses.Coords
		).where(
			dataclasses.Coords.id == coords_id
		).values(**coords)
		self.engine.execute(query)

	def edit_levels(self, levels_id: int, levels: Dict[str, str]) -> None:
		query = update(
			dataclasses.Level
		).where(
			dataclasses.Level.id == levels_id
		).values(**levels)
		self.engine.execute(query)
