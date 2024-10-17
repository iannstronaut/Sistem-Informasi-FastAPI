from fastapi import FastAPI
from services.migration import Migration
from routers import user_router, public_router, item_router


app = FastAPI()
Migration.run()

app.include_router(user_router.router)
app.include_router(public_router.router)
app.include_router(item_router.router)