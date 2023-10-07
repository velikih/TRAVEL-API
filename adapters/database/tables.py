from datetime import datetime

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
	func,
)
from sqlalchemy.orm import registry

from domain import dataclasses

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
