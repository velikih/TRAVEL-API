from fastapi import APIRouter, Response, status

from domain.service import MobileTourist
from domain.dataclasses import BodyInfo


class Controller:
	def __init__(self, service: MobileTourist):
		self.service = service
		self.router = APIRouter()
		self.router.add_api_route("/", self.test, methods=["GET"])
		self.router.add_api_route("/submitData", self.submit_data, methods=["POST"])

	def submit_data(self, body: BodyInfo, response: Response):
		try:
			id_ = self.service.add_data(body=body)
		except Exception as e:
			response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			status_now = 500
			message = e
			id_ = None
		else:
			response.status_code = status.HTTP_201_CREATED
			status_now = 201
			message = None
		finally:
			return {"status": status_now, "message": message, "id": id_}

	def test(self):
		return {'test': 'success'}
