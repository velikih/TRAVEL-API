from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any, Union

from domain import dataclasses


class UserRepo(ABC):

	@abstractmethod
	def add_user(self, user: Dict) -> int:
		...

	@abstractmethod
	def get_user_by_phone(self, user_phone: str) -> Optional[dataclasses.User]:
		...

	@abstractmethod
	def get_user_by_id(self, user_id: int) -> Optional[dataclasses.User]:
		...


class ImgRepo(ABC):

	@abstractmethod
	def add_image(self, image: Dict) -> int:
		...

	@abstractmethod
	def get_imgs_by_pereval_id(self, pereval_id: int) -> List[dataclasses.Image]:
		...

	@abstractmethod
	def edit_imgs(self, pereval_id: int, images: List[Dict[str, Any]]) -> None:
		...


class PerevalRepository(ABC):

	@abstractmethod
	def add_data(self, data_for_add: Dict):
		...

	@abstractmethod
	def add_coords(self, coords: Dict) -> int:
		...

	@abstractmethod
	def add_level(self, level: Dict) -> int:
		...

	@abstractmethod
	def get_pereval(self, pereval_id: int) -> Optional[dataclasses.PerevalAdded]:
		...

	@abstractmethod
	def get_coords_by_id(self, coords_id: int) -> Optional[dataclasses.Coords]:
		...

	@abstractmethod
	def get_levels_by_id(self, level_id: int) -> Optional[dataclasses.Level]:
		...

	@abstractmethod
	def edit_pereval(self, pereval_id: int, pereval: Dict[str, str]) -> None:
		...

	@abstractmethod
	def edit_coords(self, coords_id: int, coords: Dict[str, Union[float, int]]) -> None:
		...

	@abstractmethod
	def edit_levels(self, levels_id: int, levels: Dict[str, str]) -> None:
		...

	@abstractmethod
	def get_data_by_email(self, user_email: str) -> None:
		...
