from fastapi import FastAPI

from app.core.config import settings
from app.middleware.authMiddleware import AuthenticationMiddleware
from app.routes import auth_route, category_route, customer_route, order_route, product_route, report_route, user_route




def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(AuthenticationMiddleware)

    app.include_router(user_route.router)
    app.include_router(customer_route.router)
    app.include_router(product_route.router)
    app.include_router(category_route.router)
    app.include_router(order_route.router)
    app.include_router(report_route.router)
    app.include_router(auth_route.router )

    @app.get("/")
    def root():
        return {"message": "FastAPI Postgres App is running"}

    return app


app = create_app()
