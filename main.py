from fastapi import FastAPI, Request, HTTPException, status
from models.migration import RunMigration
from routers import api_router, public_router
from services.middleware import Middleware


app = FastAPI()
RunMigration.run()

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    try:
        # Memanggil auth middleware
        response = await Middleware.auth(request, call_next)
        return response
    except Exception as e:
        # Menangkap exception dan mengembalikan HTTPException
        print(f"Error: {e}")  # Log error ke konsol
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

app.include_router(api_router.router)
app.include_router(public_router.router)
