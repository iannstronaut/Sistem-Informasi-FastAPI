from fastapi import FastAPI
from models.migration import RunMigration
from routers import api_router, public_router


app = FastAPI()
RunMigration.run()

app.include_router(api_router.router)
app.include_router(public_router.router)
