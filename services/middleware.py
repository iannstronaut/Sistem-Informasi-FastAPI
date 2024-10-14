import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timezone

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

class Middleware:
    @staticmethod
    async def auth(request: Request, call_next):
        public_paths = ["/login", "/register", "/"]
        
        if request.url.path in public_paths:
            # Route yang tidak perlu otentikasi
            return await call_next(request)
        
        try:
            # Ambil header Authorization
            auth_header = request.headers.get("Authorization", None)
            
            # Jika header tidak ada, lempar error
            if auth_header is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization token is missing",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Jika header ada tapi format salah, tangani error
            if not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization format. Expected 'Bearer <token>'",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Ambil token dari header
            token = auth_header.split(" ")[1]
            
            # Decode JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                
            # Periksa apakah token sudah expired
            exp = payload.get("exp")
            if exp and datetime.now(timezone.utc).timestamp() > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Lanjutkan ke route berikutnya jika token valid
            response = await call_next(request)
            return response

        except JWTError as e:
            # Jika token tidak valid atau terjadi error JWT, lempar error 401
            print(f"JWTError: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            # Tangani error tak terduga lainnya dan log pesan error
            print(f"Unexpected error: {e}")
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"An error occurred: {str(e)}"
            )
