from datetime import datetime
from typing import Optional, Dict

from sqlalchemy import (
	DateTime,
	Integer,
	Unicode,
	Column,
	ForeignKey,
	Table,
	MetaData,
	Float,
	insert,
	select,
)
from sqlalchemy.orm import registry, relationship

from domain import interface, dataclasses

naming_convention = {
	'ix': 'ix_%(column_0_label)s',
	'uq': 'uq_%(table_name)s_%(column_0_name)s',
	'ck': 'ck_%(table_name)s_%(constraint_name)s',
	'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
	'pk': 'pk_%(table_name)s'
}

# даем имя схемы только для БД MSSQL, связано с инфраструктурными особенностями
metadata = MetaData(naming_convention=naming_convention)

users = Table(
	'users',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('email', Unicode(255), nullable=True),
	Column('fam', Unicode(255), nullable=False),
	Column('name', Unicode(255), nullable=False),
	Column('otc', Unicode(255), nullable=True),
	Column('phone', Unicode(255), nullable=False),
)

coords = Table(
	'coords',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('latitude', Float, nullable=False),
	Column('longitude', Float, nullable=False),
	Column('height', Integer, nullable=False),
)

levels = Table(
	'levels',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('winter', Unicode(255), nullable=False),
	Column('summer', Unicode(255), nullable=False),
	Column('autumn', Unicode(255), nullable=False),
	Column('spring', Unicode(255), nullable=False),
)

images = Table(
	'images',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('image', Unicode(255), nullable=False),
	Column('title', Unicode(255), nullable=False),
	Column('data_id', Integer, ForeignKey('data.id'), nullable=False),
)

data = Table(
	'data',
	metadata,
	Column('id', Integer, primary_key=True),
	Column('beauty_title', Unicode(255), nullable=False),
	Column('title', Unicode(255), nullable=False),
	Column('other_titles', Unicode(255), nullable=False),
	Column('connect', Unicode(255), nullable=False),
	Column('add_time', DateTime, default=datetime.utcnow()),
	Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
	Column('coords_id', Integer, ForeignKey('coords.id'), nullable=False),
	Column('level_id', Integer, ForeignKey('levels.id'), nullable=False),
)

mapper = registry()

mapper.map_imperatively(dataclasses.User, users)
mapper.map_imperatively(dataclasses.Coords, coords)
mapper.map_imperatively(dataclasses.Level, levels)
mapper.map_imperatively(
	dataclasses.Data,
	data,
	properties={
		'user': relationship(
			dataclasses.User,
			backref='data',
			lazy='joined',
		),
		'coords': relationship(
			dataclasses.Coords,
			backref='data',
			lazy='joined',
		),
		'levels': relationship(
			dataclasses.Level,
			backref='data',
			lazy='joined',
		)
	}
)
mapper.map_imperatively(
	dataclasses.Image,
	images,
	properties={
		'data': relationship(
			dataclasses.Data,
			backref='images',
			lazy='joined',
		)
	}
)


class Repository(interface.Repository):
	def __init__(self, engine):
		self.engine = engine

	def add_data(self, data_for_add: Dict) -> int:
		query = insert(dataclasses.Data, data_for_add)
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
		return self.engine.execute(query).scalars().one_or_none()
