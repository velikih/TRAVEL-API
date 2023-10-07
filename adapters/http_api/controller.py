from fastapi import APIRouter, Response, status

from domain.service import MobileTourist
from domain.interface import Repository
from domain.dataclasses import  (
	BodyInfo,
	PerevalAddedResponse,
	PerevalsByUserResponse,
	PerevalByIdResponse,
	PerevalUpdateResponse,
)


class Controller:
	def __init__(self, service: MobileTourist, repository: Repository):
		self.service = service
		self.repository = repository
		self.router = APIRouter()
		self.router.add_api_route(
			"/submitData", self.submit_data_post, methods=["POST"], response_model=PerevalAddedResponse)
		self.router.add_api_route(
			"/submitData", self.submit_data_get_all, methods=["GET"], response_model=PerevalsByUserResponse)
		self.router.add_api_route(
			"/submitData/{pereval_id}", self.submit_data_get, methods=["GET"], response_model=PerevalByIdResponse)
		self.router.add_api_route(
			"/submitData/{pereval_id}", self.submit_data_patch, methods=["PATCH"], response_model=PerevalUpdateResponse)
	def submit_data_post(self, body: BodyInfo, response: Response):
		try:
			id_ = self.service.add_data(body=body)
		except Exception as e:
			response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			status_now = 500
			message = str(e)
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
			message = str(e)
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

	def submit_data_get_all(self, user_email: str, response: Response):
		try:
			data = self.repository.get_data_by_email(user_email=user_email)
		except Exception as e:
			response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			status_now = 500
			message = str(e)
			data = None
		else:
			response.status_code = status.HTTP_200_OK
			status_now = 200
			message = None
		finally:
			return {
				"status": status_now,
				"message": message,
				"pereval_data": [elem.dict() for elem in data]
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
			if state:
				response.status_code = status.HTTP_202_ACCEPTED
				status_now = 202
			else:
				response.status_code = status.HTTP_409_CONFLICT
				status_now = 409
		finally:
			return {
				"status": status_now,
				"message": message,
				"state": state
			}
