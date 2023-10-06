from fastapi import APIRouter

from domain.service import MobileTourist
from domain.dataclasses import BodyInfo


class Controller:
	def __init__(self, service: MobileTourist):
		self.service = service
		self.router = APIRouter()
		self.router.add_api_route("/", self.test, methods=["GET"])
		self.router.add_api_route("/submitData", self.submit_data, methods=["POST"])

	def submit_data(self, body: BodyInfo):
		self.service.add_data(body=body)
		return {'added': 'success'}

	def test(self):
		return {'test': 'success'}
