from sqlalchemy import create_engine
from fastapi import FastAPI

from adapters import database, http_api
from domain import service


# logger

class Settings:
    db = database.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)
    repository = database.repository.Repository(engine=engine)


class Application:
    service = service.MobileTourist(repository=DB.repository)
    controller = http_api.Controller(service)
    app = FastAPI()
    app.include_router(controller.router)


app = Application()

if __name__ == '__main__':
    from wsgiref import simple_server

    with simple_server.make_server(host='127.0.0.1', port=8081, app=Application.app) as server:
        print('server with port 8081')
        server.serve_forever()

