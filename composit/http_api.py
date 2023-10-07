from sqlalchemy import create_engine
from fastapi import FastAPI

from adapters import database, http_api
from domain import service


# logger

class Settings:
    db = database.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.mapper.metadata.create_all(engine)

    pereval_repo = database.repository.PerevalRepository(engine=engine)
    img_repo = database.repository.ImgRepo(engine=engine)
    user_repo = database.repository.UserRepo(engine=engine)


class Application:
    service = service.MobileTourist(
        pereval_repo=DB.pereval_repo,
        img_repo=DB.img_repo,
        user_repo=DB.user_repo,
    )
    controller = http_api.Controller(service, DB.pereval_repo)
    app = FastAPI()
    app.include_router(controller.router)


app = Application()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app.app, host='127.0.0.1', port=8000)
