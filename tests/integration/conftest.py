from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapters.http_api.controller import Controller
from domain.service import MobileTourist
from domain.interface import PerevalRepository


@pytest.fixture(scope="function")
def pereval_repo(pereval, pereval_info_response, coords, user, level):
	pereval_repo = Mock(PerevalRepository)
	pereval_repo.add_data = Mock(return_value=pereval.id)
	pereval_repo.add_coords = Mock(return_value=coords.id)
	pereval_repo.add_level = Mock(return_value=level.id)
	pereval_repo.get_pereval = Mock(return_value=pereval)
	pereval_repo.get_coords_by_id = Mock(return_value=coords)
	pereval_repo.get_levels_by_id = Mock(return_value=level)
	pereval_repo.edit_pereval = Mock(return_value=None)
	pereval_repo.edit_coords = Mock(return_value=None)
	pereval_repo.edit_levels = Mock(return_value=None)
	pereval_repo.get_data_by_email = Mock(return_value=[pereval_info_response])
	return pereval_repo


@pytest.fixture(scope='function')
def mobile_tourist(pereval_info):
	mobile_tourist = Mock(MobileTourist)
	mobile_tourist.add_data = Mock(return_value=1)
	mobile_tourist.edit_pereval_data = Mock(return_value=(1, None))
	mobile_tourist.get_pereval_data = Mock(return_value=pereval_info)
	return mobile_tourist


@pytest.fixture(scope='function')
def client(mobile_tourist, pereval_repo):
	controller = Controller(service=mobile_tourist, repository=pereval_repo)
	app = FastAPI()
	app.include_router(controller.router)
	return TestClient(app)
