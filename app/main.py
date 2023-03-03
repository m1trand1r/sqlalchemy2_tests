from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.users import router as user_router
from app.endpoints.login import router as login_router

from app.core.config import settings

app = FastAPI()

app.include_router(router=user_router)
app.include_router(router=login_router)

@app.on_event('startup')
async def startup_event():
    print('start')
    

@app.on_event('shutdown')
async def shutdown_event():
    print('stop')