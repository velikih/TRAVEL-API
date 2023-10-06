from fastapi import APIRouter, Response, status

from domain.service import MobileTourist
from domain.dataclasses import BodyInfo


class Controller:
	def __init__(self, service: MobileTourist):
		self.service = service
		self.router = APIRouter()
		self.router.add_api_route("/", self.test, methods=["GET"])
		self.router.add_api_route("/submitData", self.submit_data_post, methods=["POST"])
		self.router.add_api_route("/submitData/{pereval_id}", self.submit_data_get, methods=["GET"])
		self.router.add_api_route("/submitData/{pereval_id}", self.submit_data_patch, methods=["PATCH"])

	def submit_data_post(self, body: BodyInfo, response: Response):
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

	def submit_data_get(self, pereval_id: int, response: Response):
		try:
			pereval_data = self.service.get_pereval_data(pereval_id=pereval_id)
		except Exception as e:
			response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			status_now = 500
			message = e
			pereval_data = None
		else:
			response.status_code = status.HTTP_200_OK
			status_now = 200
			message = None
		finally:
			return {
				"status": status_now,
				"message": message,
				"pereval_data": pereval_data.dict() if pereval_data is not None else None
			}

	def submit_data_patch(self, body: BodyInfo, pereval_id: int, response: Response):
		try:
			state, message = self.service.edit_pereval_data(pereval_id=pereval_id, body=body)
		except Exception as e:
			response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			status_now = 500
			message = str(e)
			state = 0
		else:
			response.status_code = status.HTTP_202_ACCEPTED
			status_now = 202
		finally:
			return {
				"status": status_now,
				"message": message,
				"state": state
			}

	def test(self):
		return {'test': 'success'}
