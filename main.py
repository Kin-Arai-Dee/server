from config.db import client
import uvicorn

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.food import food
from routes.user import user
from routes.prediction import prediction
from services.user import verify_user

COMMON_PREFIX = '/api/v1'

def create_app():
    app = FastAPI(
        title="Kin Ari Dee",
    )

    origins = ['*']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()
require_authorize = Depends(verify_user)

@app.on_event("shutdown")
def shutdown_event():
    client.close()

app.include_router(user,prefix=COMMON_PREFIX,tags=['user'])
app.include_router(prediction,prefix=f'{COMMON_PREFIX}/prediction',tags=['prediction'], dependencies=[require_authorize])
app.include_router(food,prefix=f'{COMMON_PREFIX}/food',tags=['food'], dependencies=[require_authorize])

@app.get(COMMON_PREFIX,tags=['check'])
async def check_app():
    return {"message": "API is running."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
