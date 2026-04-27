from fastapi import FastAPI

from app.core.config import settings
from app.routes import product, user, category




def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.include_router(user.router)
    app.include_router(product.router)
    app.include_router(category.router)

    @app.get("/")
    def root():
        return {"message": "FastAPI Postgres App is running"}

    return app


app = create_app()
