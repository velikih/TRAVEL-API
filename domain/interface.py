from abc import ABC, abstractmethod
from typing import Optional, Dict

from domain import dataclasses


class Repository(ABC):

	@abstractmethod
	def add_data(self, data_for_add: Dict):
		...

	@abstractmethod
	def add_user(self, user: Dict) -> int:
		...

	@abstractmethod
	def add_coords(self, coords: Dict) -> int:
		...

	@abstractmethod
	def add_level(self, level: Dict) -> int:
		...

	@abstractmethod
	def add_image(self, image: Dict) -> int:
		...

	@abstractmethod
	def get_user_by_phone(self, user_phone: str) -> Optional[dataclasses.User]:
		...
