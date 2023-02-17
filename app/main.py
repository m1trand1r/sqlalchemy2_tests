from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.users import router

from app.config import settings

app = FastAPI()

app.include_router(router=router)

@app.on_event('startup')
async def startup_event():
    print('start')
    

@app.on_event('shutdown')
async def shutdown_event():
    print('stop')